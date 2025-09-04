"""
Law firm confirmation extractor for websites
Extracts description and classifies if the site is a law firm and handles personal injury
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from supabase import Client

from .base_extractor import BaseExtractor
from ..core.config_manager import ExtractionConfig
from ..core.prompts import PromptTemplates
from ..database import create_vector_store, get_database_connection
from ..embed.chunker import DocumentChunker

logger = logging.getLogger(__name__)


class LawFirmConfirmationExtractor(BaseExtractor):
    """Extracts law firm description and classification information using RAG"""
    
    def __init__(self, config: ExtractionConfig, supabase_client: Optional[Client] = None):
        """
        Initialize law firm confirmation extractor
        
        Args:
            config: Extraction configuration
            supabase_client: Optional Supabase client
        """
        super().__init__()
        self.config = config
        self.prompts = PromptTemplates()
        
        # Get database connection
        self.db_conn = get_database_connection()
        
        # Use provided client or get from connection manager
        if supabase_client:
            self.supabase = supabase_client
        else:
            self.supabase = self.db_conn.get_supabase_client()
        
        # Initialize LLM with JSON format and token limit
        self.llm = OllamaLLM(
            model=config.model_type,
            base_url=config.ollama_base_url,
            temperature=config.temperature,
            top_p=config.top_p,
            num_predict=100,  # Hard limit for short description
            format="json"
        )
        
        # Store schema for direct API calls
        self.confirmation_schema = {
            "type": "object",
            "properties": {
                "short_description": {
                    "type": "string",
                    "description": "A single sentence describing what the organization does"
                },
                "is_law_firm": {
                    "type": "boolean",
                    "description": "Whether this is an actual law firm (not a directory or referral service)"
                },
                "is_personal_injury_firm": {
                    "type": "boolean",
                    "description": "Whether the firm handles personal injury cases"
                }
            },
            "required": ["short_description", "is_law_firm", "is_personal_injury_firm"]
        }
        
        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(
            model=config.embedder_type,
            base_url=config.ollama_base_url
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
        
        # Initialize chunker for fallback scenarios
        self.chunker = DocumentChunker(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )
        
        logger.info(f"LawFirmConfirmationExtractor initialized with model: {config.model_type}")
    
    def extract(self, markdown_content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Extract law firm confirmation from markdown content
        
        Args:
            markdown_content: The markdown text
            metadata: Optional metadata about the document
        
        Returns:
            Extracted law firm confirmation data
        """
        start_time = time.time()
        
        try:
            # Clean markdown
            cleaned_content = self.clean_markdown(markdown_content)
            
            # Create document ID from metadata
            doc_id = self._create_doc_id(metadata)
            
            # Perform extraction using vector search
            extracted_data = self._extract_with_vectors(doc_id, cleaned_content)
            
            # Add metadata
            extraction_time = time.time() - start_time
            extracted_data['_metadata'] = {
                'extraction_time_seconds': extraction_time,
                'source_url': metadata.get('url') if metadata else None,
                'timestamp': datetime.now().isoformat()
            }
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            return {
                'error': str(e),
                '_metadata': {
                    'extraction_time_seconds': time.time() - start_time,
                    'timestamp': datetime.now().isoformat()
                }
            }
    
    def extract_from_domain(self, domain: str) -> Dict[str, Any]:
        """
        Extract law firm confirmation from homepage/index of a domain
        
        Args:
            domain: Domain name to extract from
        
        Returns:
            Extracted law firm confirmation data
        """
        # For law firm confirmation, we want to focus on homepage content
        # Use domain/index or domain/home as document ID pattern
        doc_id = f"{domain}/extraction"
        return self._extract_with_vectors(doc_id, "", search_homepage_only=True)
    
    def extract_from_document(self, document_id: str) -> Dict[str, Any]:
        """
        Extract law firm confirmation from a specific document
        
        Args:
            document_id: Document ID to extract from
        
        Returns:
            Extracted law firm confirmation data
        """
        return self._extract_with_vectors(document_id, "", search_homepage_only=False)
    
    def _create_doc_id(self, metadata: Optional[Dict]) -> str:
        """Create document ID from metadata"""
        if metadata and 'url' in metadata:
            return metadata['url']
        elif metadata and 'domain' in metadata:
            return f"{metadata['domain']}/{datetime.now().timestamp()}"
        elif metadata and 'source' in metadata:
            return metadata['source']
        else:
            return str(datetime.now().timestamp())
    
    def _extract_with_vectors(self, doc_id: str, full_content: str, 
                              search_homepage_only: bool = True) -> Dict[str, Any]:
        """
        Perform extraction using vector search
        
        Args:
            doc_id: Document identifier
            full_content: Full document content for fallback
            search_homepage_only: Whether to search only homepage content
        
        Returns:
            Extracted law firm confirmation data
        """
        # Query for law firm and personal injury related content
        query = "law firm attorney lawyer legal services personal injury accident compensation practice areas about us"
        
        # Extract domain for filtering
        domain = self.chunker._extract_domain_from_id(doc_id)
        
        try:
            # Build search filter
            search_filter = {}
            
            if domain:
                import hashlib
                # Hash domain directly (with periods)
                domain_id = hashlib.md5(domain.encode()).hexdigest()[:12]
                
                if search_homepage_only:
                    # Try to filter for homepage content specifically
                    # Look for documents with index, home, or about in the path
                    search_filter = {
                        'domain_id': domain_id,
                        '$or': [
                            {'document_id': {'$ilike': f'%{domain}/index%'}},
                            {'document_id': {'$ilike': f'%{domain}/home%'}},
                            {'document_id': {'$ilike': f'%{domain}/about%'}},
                            {'document_id': {'$ilike': f'%{domain}/%'}}  # Fallback to any page
                        ]
                    }
                else:
                    search_filter = {'domain_id': domain_id}
                
                logger.info(f"Searching for law firm confirmation in domain: {domain}")
            else:
                search_filter = {'document_id': doc_id}
                logger.info(f"Searching document: {doc_id}")
            
            # For Supabase/simple stores, use simpler filter
            if not hasattr(self.vector_store, 'similarity_search_with_metadata_boost'):
                search_filter = {'domain_id': domain_id} if domain else {'document_id': doc_id}
            
            # Search for relevant chunks
            if hasattr(self.vector_store, 'similarity_search_with_metadata_boost'):
                # Use boosted search for local store
                relevant_docs = self.vector_store.similarity_search_with_metadata_boost(
                    query=query,
                    k=3,  # Use fewer chunks for description
                    filter=search_filter,
                    boost_field='contains_addresses'  # Still use boost but not as relevant
                )
            else:
                # Regular search for Supabase
                relevant_docs = self.vector_store.similarity_search(
                    query=query,
                    k=3,  # Use fewer chunks for description
                    filter=search_filter
                )
            
            logger.info(f"Retrieved {len(relevant_docs)} relevant chunks for law firm confirmation")
            
            # Extract text from documents
            chunks = []
            chunk_ids = []
            for i, doc in enumerate(relevant_docs):
                content = doc.page_content
                chunks.append(content)
                
                # Get chunk ID from metadata
                chunk_id = "unknown"
                if hasattr(doc, 'metadata'):
                    chunk_id = doc.metadata.get('id', doc.metadata.get('chunk_id', 'unknown'))
                    # Log which document the chunk came from
                    doc_id_from_chunk = doc.metadata.get('document_id', 'unknown')
                    logger.debug(f"Chunk {i+1} from document: {doc_id_from_chunk}")
                chunk_ids.append(chunk_id)
            
        except Exception as e:
            logger.warning(f"Vector search failed, using fallback: {str(e)}")
            # Fallback to using full content
            chunks = self.chunker.chunk_text(full_content)[:3]
            chunk_ids = ["fallback_chunk"] * len(chunks)
        
        # Generate extraction prompt
        system_prompt = self.prompts.get_system_prompt()
        extraction_prompt = self.prompts.get_law_firm_confirmation_prompt("\n---\n".join(chunks))
        
        # Log prompt sizes
        logger.debug(f"Combined prompt length: {len(system_prompt) + len(extraction_prompt)} chars")
        
        # Call LLM with retry logic
        for attempt in range(self.config.retry_attempts):
            try:
                # Use direct Ollama API call with schema enforcement
                import requests
                ollama_url = f"{self.config.ollama_base_url}/api/generate"
                
                # Build options dict with model parameters
                options = {
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "seed": self.config.seed,
                    "num_ctx": self.config.num_ctx if self.config.num_ctx is not None else 8192,
                    "num_predict": 150  # Token limit for confirmation response
                }
                
                payload = {
                    "model": self.config.model_type,
                    "system": system_prompt,
                    "prompt": extraction_prompt,
                    "format": self.confirmation_schema,
                    "options": options,
                    "stream": False,
                    "keep_alive": 0
                }
                
                response_obj = requests.post(ollama_url, json=payload)
                if response_obj.status_code == 200:
                    response_data = response_obj.json()
                    response = response_data['response']
                    
                    # Log token usage
                    if 'eval_count' in response_data:
                        output_tokens = response_data['eval_count']
                        logger.debug(f"Output tokens: {output_tokens}")
                else:
                    # Fallback to LangChain if direct API fails
                    logger.warning(f"Direct Ollama API failed, using LangChain: {response_obj.status_code}")
                    full_prompt = f"{system_prompt}\n\n{extraction_prompt}"
                    response = self.llm.invoke(full_prompt)
                
                # Parse JSON response
                extracted_data = self._parse_llm_response(response)
                logger.info(f"Extracted law firm confirmation: {extracted_data}")
                
                if extracted_data and 'short_description' in extracted_data and 'is_law_firm' in extracted_data:
                    # Add chunk IDs to the result
                    extracted_data['_chunk_ids'] = chunk_ids
                    return extracted_data
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.config.retry_attempts - 1:
                    raise
        
        return {'short_description': '', 'is_law_firm': False, 'is_personal_injury_firm': False, '_chunk_ids': chunk_ids if 'chunk_ids' in locals() else []}
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM JSON response"""
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
            return {}