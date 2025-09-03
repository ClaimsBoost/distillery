"""
Office location extractor using RAG (Retrieval-Augmented Generation)
Simplified extraction pipeline focused on office locations
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


class OfficeExtractor(BaseExtractor):
    """Extracts office locations using RAG with vector search"""
    
    def __init__(self, config: ExtractionConfig, supabase_client: Optional[Client] = None):
        """
        Initialize office extractor
        
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
        
        # Initialize LLM with JSON format
        # Note: LangChain's OllamaLLM doesn't support schema directly,
        # we'll need to use the Ollama API directly or modify our approach
        self.llm = OllamaLLM(
            model=config.model_type,
            base_url=config.ollama_base_url,
            temperature=config.temperature,
            top_p=config.top_p,
            num_predict=config.max_tokens,
            format="json"  # Basic JSON format
        )
        
        # Store schema for direct API calls if needed
        self.office_schema = {
            "type": "object",
            "properties": {
                "offices": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["offices"]
        }
        
        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(
            model=config.embedder_type,
            base_url=config.ollama_base_url
        )
        
        # Initialize vector store
        # Only pass supabase_client if we're not using local database
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
        
        logger.info(f"OfficeExtractor initialized with model: {config.model_type}")
    
    def extract(self, markdown_content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Extract office locations from markdown content
        
        Args:
            markdown_content: The markdown text
            metadata: Optional metadata about the document
        
        Returns:
            Extracted office locations
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
        Extract office locations from all documents in a domain
        
        Args:
            domain: Domain name to extract from
        
        Returns:
            Extracted office locations
        """
        doc_id = f"{domain}/extraction"
        return self._extract_with_vectors(doc_id, "", search_domain_wide=True)
    
    def extract_from_document(self, document_id: str) -> Dict[str, Any]:
        """
        Extract office locations from a specific document
        
        Args:
            document_id: Document ID to extract from
        
        Returns:
            Extracted office locations
        """
        return self._extract_with_vectors(document_id, "", search_domain_wide=False)
    
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
                              search_domain_wide: bool = True) -> Dict[str, Any]:
        """
        Perform extraction using vector search
        
        Args:
            doc_id: Document identifier
            full_content: Full document content for fallback
            search_domain_wide: Whether to search across domain or just document
        
        Returns:
            Extracted office data
        """
        # Query for office-related chunks
        query = "office location street address city state zip phone"
        
        # Extract domain for filtering
        domain = self.chunker._extract_domain_from_id(doc_id)
        
        try:
            # Build search filter
            search_filter = {}
            
            if search_domain_wide and domain:
                import hashlib
                # Convert domain to underscore format to match database
                domain_for_hash = domain.replace('.', '_')
                domain_id = hashlib.md5(domain_for_hash.encode()).hexdigest()[:12]
                search_filter = {'domain_id': domain_id}
                logger.info(f"Searching across domain: {domain} (using {domain_for_hash} for hash)")
            else:
                search_filter = {'document_id': doc_id}
                logger.info(f"Searching document: {doc_id}")
            
            # Search for relevant chunks
            if hasattr(self.vector_store, 'similarity_search_with_metadata_boost'):
                # Use boosted search for local store
                relevant_docs = self.vector_store.similarity_search_with_metadata_boost(
                    query=query,
                    k=self.config.k_chunks,
                    filter=search_filter,
                    boost_field='contains_addresses'
                )
            else:
                # Regular search for Supabase
                relevant_docs = self.vector_store.similarity_search(
                    query=query,
                    k=self.config.k_chunks,
                    filter=search_filter
                )
            
            logger.info(f"Retrieved {len(relevant_docs)} relevant chunks")
            
            # Extract text from documents and log full chunks with IDs
            chunks = []
            chunk_ids = []
            for i, doc in enumerate(relevant_docs):
                content = doc.page_content
                chunks.append(content)
                
                # Get chunk ID from metadata
                chunk_id = "unknown"
                if hasattr(doc, 'metadata'):
                    chunk_id = doc.metadata.get('id', doc.metadata.get('chunk_id', 'unknown'))
                chunk_ids.append(chunk_id)
                
                # Log FULL chunk content and ID
                logger.info(f"=== CHUNK {i+1} ID: {chunk_id} ===")
                logger.info(f"FULL CONTENT:\n{content}")
                logger.info(f"=== END CHUNK {i+1} ===")
            
            # Log retrieval details
            if relevant_docs and domain:
                docs_found = set()
                for doc in relevant_docs:
                    if hasattr(doc, 'metadata') and 'document_id' in doc.metadata:
                        docs_found.add(doc.metadata['document_id'])
                logger.debug(f"Chunks from {len(docs_found)} documents")
            
        except Exception as e:
            logger.warning(f"Vector search failed, using fallback: {str(e)}")
            # Fallback to using full content
            chunks = self.chunker.chunk_text(full_content)[:self.config.k_chunks]
            chunk_ids = ["fallback_chunk"] * len(chunks)
        
        # Generate extraction prompt (now separated into system and user parts)
        system_prompt = self.prompts.get_system_prompt()
        extraction_prompt = self.prompts.get_office_extraction_prompt("\n---\n".join(chunks))
        
        # Log prompt sizes
        logger.info(f"System prompt length: {len(system_prompt)} chars")
        logger.info(f"Extraction prompt length: {len(extraction_prompt)} chars")
        logger.info(f"Combined prompt length: {len(system_prompt) + len(extraction_prompt)} chars (~{(len(system_prompt) + len(extraction_prompt))//4} tokens)")
        
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
                    "num_ctx": self.config.num_ctx if self.config.num_ctx is not None else 8192,  # Context window in options
                }
                
                payload = {
                    "model": self.config.model_type,
                    "system": system_prompt,  # System prompt now separate
                    "prompt": extraction_prompt,  # User/extraction prompt only
                    "format": self.office_schema,
                    "options": options,  # Model options including num_ctx
                    "stream": False,
                    "keep_alive": 0  # Reset context after each request to prevent cross-domain contamination
                }
                
                logger.info(f"Setting num_ctx to: {options['num_ctx']} (in options)")
                
                # Save payload for debugging
                with open('/tmp/ollama_payload.json', 'w') as f:
                    json.dump(payload, f, indent=2)
                logger.info(f"Saved Ollama payload to /tmp/ollama_payload.json")
                
                logger.debug(f"Ollama API payload: {json.dumps(payload, indent=2)[:500]}...")
                response_obj = requests.post(ollama_url, json=payload)
                if response_obj.status_code == 200:
                    response_data = response_obj.json()
                    response = response_data['response']
                    
                    # Log token usage
                    if 'prompt_eval_count' in response_data and 'eval_count' in response_data:
                        input_tokens = response_data['prompt_eval_count']
                        output_tokens = response_data['eval_count']
                        total_tokens = input_tokens + output_tokens
                        logger.info(f"Token usage - Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}")
                else:
                    # Fallback to LangChain if direct API fails
                    logger.warning(f"Direct Ollama API failed, using LangChain: {response_obj.status_code}")
                    # Combine prompts for LangChain fallback
                    full_prompt = f"{system_prompt}\n\n{extraction_prompt}"
                    response = self.llm.invoke(full_prompt)
                
                # Parse JSON response
                logger.info(f"Raw LLM response (first 1000 chars): {response[:1000]}")
                extracted_data = self._parse_llm_response(response)
                logger.info(f"Parsed data: {extracted_data}")
                logger.debug(f"Raw LLM response: {response[:500]}")
                logger.debug(f"Parsed data: {extracted_data}")
                
                if extracted_data:
                    # Validate and fix structure
                    if hasattr(self.prompts, 'validate_extraction'):
                        validation = self.prompts.validate_extraction(extracted_data)
                        if not validation['valid']:
                            logger.warning(f"Attempt {attempt + 1}: Validation failed - {validation['errors']}")
                            if hasattr(self.prompts, 'fix_extraction_structure'):
                                extracted_data = self.prompts.fix_extraction_structure(extracted_data)
                                validation = self.prompts.validate_extraction(extracted_data)
                                if validation['valid']:
                                    logger.info("Successfully fixed structure")
                                    # Add chunk IDs to the result
                                    extracted_data['_chunk_ids'] = chunk_ids
                                    return extracted_data
                            continue
                        else:
                            # Add chunk IDs to the result
                            extracted_data['_chunk_ids'] = chunk_ids
                            return extracted_data
                    else:
                        # Add chunk IDs to the result
                        extracted_data['_chunk_ids'] = chunk_ids
                        return extracted_data
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.config.retry_attempts - 1:
                    raise
        
        return {'_chunk_ids': chunk_ids if 'chunk_ids' in locals() else []}
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM JSON response"""
        try:
            # With format="json", Ollama returns valid JSON directly
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