"""
Base extractor class with shared LLM functionality, schema support, and API request storage
"""

import json
import logging
import os
import re
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, ClassVar
from enum import Enum
from pathlib import Path
from datetime import datetime
import hashlib

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from supabase import Client

from ..core.settings import get_settings, Settings
from ..core.prompts import PromptTemplates
from ..database import create_vector_store, get_database_connection
from ..embed.chunker import DocumentChunker

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """Base class with shared LLM, schema support, and API request storage"""

    # Single shared LLM instance for all extractors
    _shared_llm: ClassVar[Optional[OllamaLLM]] = None

    # Cache for config modules
    _config_cache: ClassVar[Dict[str, Any]] = {}

    def __init__(self, settings: Settings = None, supabase_client: Optional[Client] = None):
        """
        Initialize enhanced extractor with shared components

        Args:
            settings: Application settings (uses global if not provided)
            supabase_client: Optional Supabase client
        """
        super().__init__()
        self.settings = settings or get_settings()
        self.prompts = PromptTemplates()

        # Get database connection
        self.db_conn = get_database_connection()

        # Use provided client or get from connection manager
        if supabase_client:
            self.supabase = supabase_client
        else:
            self.supabase = self.db_conn.get_supabase_client()

        # Initialize or get shared LLM instance
        self.llm = self._get_or_create_llm()

        # Initialize embeddings (these are lightweight, ok to have per instance)
        self.embeddings = OllamaEmbeddings(
            model=self.settings.extraction.embedder_type,
            base_url=self.settings.ollama.base_url
        )

        # Initialize vector store
        if self.db_conn.is_local:
            self.vector_store = create_vector_store(
                config={'use_local': True},
                embeddings=self.embeddings,
                supabase_client=None
            )
        else:
            self.vector_store = create_vector_store(
                config={'use_local': False},
                embeddings=self.embeddings,
                supabase_client=self.supabase
            )

        # Initialize chunker
        self.chunker = DocumentChunker(
            chunk_size=self.settings.extraction.chunk_size,
            chunk_overlap=self.settings.extraction.chunk_overlap
        )

        logger.info(f"{self.__class__.__name__} initialized with model: {self.settings.extraction.model_type}")

    def _get_or_create_llm(self) -> OllamaLLM:
        """
        Get or create the single shared LLM instance

        Returns:
            Shared OllamaLLM instance
        """
        # Create single shared instance if it doesn't exist
        if BaseExtractor._shared_llm is None:
            BaseExtractor._shared_llm = OllamaLLM(
                model=self.settings.extraction.model_type,
                base_url=self.settings.ollama.base_url,
                # Don't set variable parameters here - they'll be set per request
                # Only set connection-level settings
                format="json"  # All extractors use JSON format
            )
            logger.info(f"Created single shared LLM instance for model: {self.settings.extraction.model_type}")

        return BaseExtractor._shared_llm

    def _get_num_predict(self) -> int:
        """
        Get the appropriate num_predict value based on expected output size

        Returns:
            Number of tokens to predict
        """
        # Get OUTPUT_SIZE from config or fall back to settings
        try:
            config = self._get_config()
            return config.OUTPUT_SIZE
        except:
            return self.settings.extraction.max_tokens

    def clean_markdown(self, markdown_content: str) -> str:
        """
        Clean and normalize markdown content

        Args:
            markdown_content: Raw markdown text

        Returns:
            Cleaned markdown text
        """
        # Remove excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', markdown_content)

        # Remove markdown image tags but keep alt text
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', content)

        # Normalize whitespace
        content = ' '.join(content.split())

        return content

    def _load_prompt(self) -> str:
        """
        Load the prompt template for this extractor from its directory

        Returns:
            Prompt template string
        """
        # Find the extractor's directory
        extractor_dir = Path(__file__).parent / "extractors" / self.extraction_name
        prompt_file = extractor_dir / "prompt.md"

        if not prompt_file.exists():
            logger.error(f"Prompt file not found: {prompt_file}")
            raise FileNotFoundError(f"Prompt file not found for {self.extraction_name}")

        return prompt_file.read_text()

    def extract(self, markdown_content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Extract structured data from markdown content with API request tracking

        Args:
            markdown_content: The markdown text to extract from
            metadata: Optional metadata about the document

        Returns:
            Extracted data with API request included
        """
        if not markdown_content:
            return {"error": "No content provided"}

        try:
            # Load the prompt template from the extractor's directory
            prompt_template = self._load_prompt()

            # Replace the content placeholder
            prompt = prompt_template.replace("{content}", markdown_content[:30000])

        except FileNotFoundError as e:
            logger.error(f"Failed to load prompt: {str(e)}")
            return {"error": f"No prompt file for {self.extraction_name}"}

        # Call Ollama API with schema
        response_data, api_payload = self._call_ollama_api(prompt)

        if "response" in response_data:
            result = self._parse_json_result(response_data["response"])
            if result:
                # Add the API request to the result for storage
                result['_api_request'] = api_payload
                # Add chunk IDs if provided in metadata
                if metadata and 'chunk_ids' in metadata:
                    result['chunk_ids'] = metadata['chunk_ids']
                return result

        return {"error": "Failed to extract data"}

    def _get_config(self):
        """
        Get the config module for this extractor

        Returns:
            The config module for the current extractor
        """
        # Get the module path from the class
        module_path = self.__class__.__module__
        # Convert to config module path (e.g., src.extract.extractors.awards.extractor -> src.extract.extractors.awards.config)
        # Remove the last part (extractor) and add config
        parts = module_path.rsplit('.', 1)
        if len(parts) == 2:
            config_path = f"{parts[0]}.config"
        else:
            config_path = module_path + '.config'

        # Check cache first
        if config_path not in BaseExtractor._config_cache:
            import importlib
            BaseExtractor._config_cache[config_path] = importlib.import_module(config_path)

        return BaseExtractor._config_cache[config_path]

    @property
    def extraction_name(self) -> str:
        """
        Get the name of this extraction type

        Returns:
            Name of the extraction (e.g., 'attorneys', 'office_locations')
        """
        config = self._get_config()
        return config.EXTRACTOR_NAME

    def extract_from_domain(self, domain: str, chunks_only: bool = False) -> Dict[str, Any]:
        """
        Extract data from an entire domain

        Args:
            domain: Domain name to extract from
            chunks_only: Whether to return only the chunks without extraction

        Returns:
            Extracted data
        """
        # Get config using the cached method
        config = self._get_config()

        # Search for relevant chunks using config values
        boost_field = getattr(config, 'BOOST_FIELD', None)
        chunks = self._search_relevant_chunks(
            config.SEARCH_QUERY,
            domain,
            k=config.CHUNK_COUNT,
            boost_field=boost_field
        )

        if chunks_only:
            return {"chunks": [{"content": doc.page_content, "metadata": doc.metadata} for doc in chunks]}

        # Combine chunk content - take up to 10 chunks
        chunks_to_use = chunks[:10]
        combined_content = "\n\n".join([doc.page_content for doc in chunks_to_use])

        # Extract chunk IDs from metadata
        chunk_ids = [doc.metadata.get('id') for doc in chunks_to_use if doc.metadata.get('id')]

        # Extract using the base extract method
        return self.extract(combined_content, {"domain": domain, "chunk_ids": chunk_ids})

    def extract_from_document(self, document_id: str) -> Dict[str, Any]:
        """
        Extract data from a specific document

        Args:
            document_id: Document ID to extract from

        Returns:
            Extracted data
        """
        # Get config using the cached method
        config = self._get_config()

        # Search for relevant chunks using config values
        boost_field = getattr(config, 'BOOST_FIELD', None)
        chunks = self._search_relevant_chunks(
            config.SEARCH_QUERY,
            document_id,
            k=config.CHUNK_COUNT,
            boost_field=boost_field
        )

        # Combine chunk content - take up to 10 chunks
        chunks_to_use = chunks[:10]
        combined_content = "\n\n".join([doc.page_content for doc in chunks_to_use])

        # Extract chunk IDs from metadata
        chunk_ids = [doc.metadata.get('id') for doc in chunks_to_use if doc.metadata.get('id')]

        # Extract using the base extract method
        return self.extract(combined_content, {"document_id": document_id, "chunk_ids": chunk_ids})

    def _load_extraction_schema(self) -> Optional[Dict[str, Any]]:
        """
        Load the JSON schema for this extractor

        Returns:
            Schema dictionary or None if not found
        """
        try:
            # Look in the new modular structure
            schema_path = Path(__file__).parent / "extractors" / self.extraction_name / "schema.json"
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    return json.load(f)
            else:
                # Schema is optional - don't warn if not found
                logger.debug(f"No schema file at: {schema_path}")
                return None
        except Exception as e:
            logger.error(f"Failed to load schema: {str(e)}")
            return None

    def _call_ollama_api(self, prompt: str, system_prompt: str = "") -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Call Ollama API directly with schema support and per-request parameters

        Args:
            prompt: The extraction prompt
            system_prompt: System prompt

        Returns:
            Tuple of (response_data, request_payload)
        """
        ollama_url = f"{self.settings.ollama.base_url}/api/generate"

        # Load schema for this extractor
        schema = self._load_extraction_schema()

        # Build options dict with ALL parameters set per request
        options = {
            "temperature": self.settings.extraction.temperature,
            "top_p": self.settings.extraction.top_p,
            "seed": self.settings.extraction.seed,
            "num_ctx": self.settings.extraction.num_ctx,
            "num_predict": self._get_num_predict()  # Varies by extractor type
        }

        # Build payload
        payload = {
            "model": self.settings.extraction.model_type,
            "prompt": prompt,
            "system": system_prompt if system_prompt else self.prompts.get_system_prompt(),
            "format": schema if schema else "json",  # Use schema if available
            "options": options,
            "stream": False,
            "keep_alive": 0  # Reset context after each request
        }

        # Store timestamp
        payload['_request_timestamp'] = datetime.now().isoformat()

        # Log what extractor and output size is being used
        logger.debug(f"{self.extraction_name} using num_predict={options['num_predict']} tokens")

        try:
            response = requests.post(ollama_url, json=payload, timeout=120)
            response.raise_for_status()
            response_data = response.json()

            # Log token usage if available
            if 'prompt_eval_count' in response_data and 'eval_count' in response_data:
                logger.info(f"[{self.extraction_name}] Token usage - Input: {response_data['prompt_eval_count']}, "
                           f"Output: {response_data['eval_count']}, "
                           f"Total: {response_data['prompt_eval_count'] + response_data['eval_count']}")

            return response_data, payload

        except Exception as e:
            logger.error(f"Ollama API call failed: {str(e)}")
            # Fall back to using shared LLM with invoke
            # Note: When using invoke, we should also pass parameters
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

            # For fallback, we could potentially use the shared LLM with custom parameters
            # but LangChain's invoke doesn't easily support per-call parameter override
            # So we'll just use it as-is for now
            response = self.llm.invoke(full_prompt)
            return {"response": response}, payload


    def _search_relevant_chunks(self, query: str, doc_or_domain: str, k: int = 3, boost_field: Optional[str] = None) -> list:
        """
        Search for relevant chunks using vector similarity with optional metadata boosting

        Args:
            query: Search query
            doc_or_domain: Document ID or domain name
            k: Number of chunks to retrieve
            boost_field: Optional metadata field to boost ('addresses', 'money', 'emails', 'phone_numbers')

        Returns:
            List of relevant document chunks
        """
        try:
            # Determine if we're searching by domain or document
            if '/' in doc_or_domain or '.' in doc_or_domain:
                # This looks like a domain
                domain = self.chunker._extract_domain_from_id(doc_or_domain)
                if domain:
                    # Hash domain directly (with periods)
                    domain_id = hashlib.md5(domain.encode()).hexdigest()[:12]
                    search_filter = {'domain_id': domain_id}
                    logger.info(f"Searching domain: {domain}")
                else:
                    search_filter = {'document_id': doc_or_domain}
                    logger.info(f"Searching document: {doc_or_domain}")
            else:
                # Assume it's a document ID
                search_filter = {'document_id': doc_or_domain}
                logger.info(f"Searching document: {doc_or_domain}")

            # Use metadata-boosted search if available and boost_field is specified
            if boost_field and hasattr(self.vector_store, 'similarity_search_with_metadata_boost'):
                results = self.vector_store.similarity_search_with_metadata_boost(
                    query=query,
                    k=k,
                    filter=search_filter,
                    boost_field=f'contains_{boost_field}'  # e.g., 'contains_addresses'
                )
                logger.info(f"Used metadata-boosted search for {boost_field}")
            else:
                # Regular search
                results = self.vector_store.similarity_search(
                    query,
                    k=k,
                    filter=search_filter
                )

            logger.info(f"Retrieved {len(results)} chunks")
            return results

        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            return []

    def _parse_json_result(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON from LLM response

        Args:
            response: LLM response string

        Returns:
            Parsed JSON or None
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed: {str(e)}")

            # Try to extract JSON from response
            try:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass

            logger.error("Failed to parse JSON from LLM response")
            return None

    def _extract_with_api(self, content: str, domain: str) -> Dict[str, Any]:
        """
        Extract using direct Ollama API with schema support and request storage

        Args:
            content: Content to extract from
            domain: Domain for storage

        Returns:
            Extraction result
        """
        # Use the main extract method which handles API request tracking
        metadata = {'domain': domain}
        return self.extract(content, metadata)