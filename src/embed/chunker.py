"""
Document chunking utilities
Provides consistent chunking across embedding and extraction
"""

import hashlib
import logging
from typing import List, Dict, Any, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from .pattern_detector import PatternDetector

logger = logging.getLogger(__name__)


class DocumentChunker:
    """Handles document chunking with metadata enhancement"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Initialize document chunker
        
        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        logger.info(f"DocumentChunker initialized: size={chunk_size}, overlap={chunk_overlap}")
    
    def chunk_document(self, content: str, doc_id: str, 
                      domain: Optional[str] = None,
                      additional_metadata: Optional[Dict] = None) -> List[Document]:
        """
        Split document into chunks with metadata
        
        Args:
            content: Document content
            doc_id: Document identifier
            domain: Optional domain name
            additional_metadata: Optional extra metadata to include
        
        Returns:
            List of Document objects with metadata
        """
        # Split text into chunks
        texts = self.text_splitter.split_text(content)
        
        # Extract domain if not provided
        if not domain:
            domain = self._extract_domain_from_id(doc_id)
        
        # Create Document objects with metadata
        documents = []
        for i, text in enumerate(texts):
            # Detect patterns in chunk
            pattern_metadata = PatternDetector.detect_patterns(text)
            
            # Build metadata
            metadata = {
                'document_id': doc_id,
                'chunk_index': i,
                'total_chunks': len(texts),
                **pattern_metadata
            }
            
            # Add domain info if available
            if domain:
                metadata['domain'] = domain
                metadata['domain_id'] = hashlib.md5(domain.encode()).hexdigest()[:12]
            
            # Add any additional metadata
            if additional_metadata:
                metadata.update(additional_metadata)
            
            doc = Document(
                page_content=text,
                metadata=metadata
            )
            documents.append(doc)
        
        logger.info(f"Created {len(documents)} chunks from document {doc_id}" + 
                   (f" for domain {domain}" if domain else ""))
        return documents
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Simple text chunking without metadata
        
        Args:
            text: Text to chunk
        
        Returns:
            List of text chunks
        """
        return self.text_splitter.split_text(text)
    
    def _extract_domain_from_id(self, doc_id: str) -> Optional[str]:
        """
        Extract domain from document ID
        
        Args:
            doc_id: Document identifier
        
        Returns:
            Domain name if found
        """
        from urllib.parse import urlparse
        
        # Check if doc_id looks like a URL
        if doc_id.startswith('http://') or doc_id.startswith('https://'):
            parsed = urlparse(doc_id)
            return parsed.netloc.lower()
        
        # Check if doc_id contains a domain pattern
        if '/' in doc_id:
            # Might be domain/path format (e.g., "137law.com/index.md")
            potential_domain = doc_id.split('/')[0]
            if '.' in potential_domain:
                return potential_domain.lower()
        
        # Check if the whole doc_id looks like a domain
        if '.' in doc_id:
            # Likely a domain like "137law.com"
            return doc_id.lower()
        
        return None