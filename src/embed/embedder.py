"""
Document embedder for vector database storage
Simplified to use new database and chunker modules
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from langchain_ollama import OllamaEmbeddings
from psycopg2.extras import Json

from ..core.storage_handler import StorageHandler
from ..core.settings import get_settings, Settings
from ..database import get_database_connection
from .chunker import DocumentChunker

logger = logging.getLogger(__name__)


class DocumentEmbedder:
    """Handles document embedding into vector database"""
    
    def __init__(self, settings: Settings = None, storage_config: Optional[Dict] = None):
        """
        Initialize document embedder
        
        Args:
            settings: Application settings (uses global if not provided)
            storage_config: Optional storage configuration
        """
        self.settings = settings or get_settings()
        
        # Initialize storage handler
        if storage_config:
            self.storage = StorageHandler(storage_config)
        else:
            self.storage = StorageHandler({
                'bucket': 'law-firm-html',
                'base_path': 'markdown'
            })
        
        # Initialize embeddings model
        self.embeddings = OllamaEmbeddings(
            model=self.settings.extraction.embedder_type,
            base_url=self.settings.ollama.base_url
        )
        
        # Initialize chunker
        self.chunker = DocumentChunker(
            chunk_size=self.settings.extraction.chunk_size,
            chunk_overlap=self.settings.extraction.chunk_overlap
        )
        
        # Get database connection
        self.db_conn = get_database_connection()
        
        logger.info(f"DocumentEmbedder initialized with model: {self.settings.extraction.embedder_type}")
    
    def embed_file(self, file_path: str, force: bool = False) -> Dict[str, Any]:
        """
        Embed a single markdown file
        
        Args:
            file_path: Path to markdown file
            force: Whether to re-embed if already exists
        
        Returns:
            Embedding result summary
        """
        logger.info(f"Embedding file: {file_path}")
        
        # Read file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract domain from filename
        filename = Path(file_path).name
        domain = self._extract_domain_from_filename(filename)
        
        document = {
            'domain': domain,
            'filename': filename,
            'content': content,
            'document_id': f"{domain}/{filename}"
        }
        
        return self._embed_documents([document], force)
    
    def embed_domain(self, domain: str, force: bool = False, 
                    max_files: Optional[int] = None) -> Dict[str, Any]:
        """
        Embed all markdown files for a domain
        
        Args:
            domain: Domain name (e.g., '137law.com')
            force: Whether to re-embed if already exists
            max_files: Optional limit on number of files
        
        Returns:
            Embedding result summary
        """
        logger.info(f"Embedding domain: {domain}")
        
        # Download all markdown files for the domain
        files = self.storage.list_files_for_domain(domain)
        
        if not files:
            logger.error(f"No files found for domain {domain}")
            return {
                'success': False,
                'error': f'No files found for domain {domain}',
                'domain': domain
            }
        
        logger.info(f"Found {len(files)} files for domain {domain}")
        
        # Limit files if requested
        if max_files:
            files = files[:max_files]
            logger.info(f"Limited to {max_files} files")
        
        # Download and prepare documents
        documents = []
        for filename in files:
            content = self.storage.download_file(domain, filename)
            if content:
                documents.append({
                    'domain': domain,
                    'filename': filename,
                    'content': content,
                    'document_id': f"{domain}/{filename}"
                })
        
        return self._embed_documents(documents, force)
    
    def verify_embeddings(self, domain: str) -> Dict[str, Any]:
        """
        Verify embeddings are stored for a domain
        
        Args:
            domain: Domain name to verify
        
        Returns:
            Verification results
        """
        if not self.db_conn.is_local:
            return {'error': 'Verification only available for local database'}
        
        try:
            with self.db_conn.get_postgres_connection() as (conn, cur):
                # Count chunks for domain
                cur.execute("SELECT COUNT(*) FROM document_vectors WHERE domain = %s", (domain,))
                count = cur.fetchone()[0]
                
                # Get unique document IDs
                cur.execute("""
                    SELECT DISTINCT document_id 
                    FROM document_vectors 
                    WHERE domain = %s
                    LIMIT 10
                """, (domain,))
                doc_ids = [row[0] for row in cur.fetchall()]
                
                return {
                    'domain': domain,
                    'chunk_count': count,
                    'document_count': len(doc_ids),
                    'sample_documents': doc_ids[:5]
                }
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return {'error': str(e)}
    
    def clear_domain(self, domain: str) -> Dict[str, Any]:
        """
        Clear all embeddings for a domain
        
        Args:
            domain: Domain name to clear
        
        Returns:
            Result with number of deleted records
        """
        if not self.db_conn.is_local:
            return {'error': 'Clear only available for local database'}
        
        try:
            deleted = self.db_conn.execute_query(
                "DELETE FROM document_vectors WHERE domain = %s",
                (domain,),
                fetch=False
            )
            
            logger.info(f"Cleared {deleted} embeddings for domain {domain}")
            
            return {
                'success': True,
                'domain': domain,
                'deleted': deleted
            }
        except Exception as e:
            logger.error(f"Clear failed: {str(e)}")
            return {'error': str(e)}
    
    def _embed_documents(self, documents: List[Dict[str, Any]], 
                        force: bool = False) -> Dict[str, Any]:
        """
        Internal method to embed documents
        
        Args:
            documents: List of document dictionaries
            force: Whether to re-embed existing documents
        
        Returns:
            Embedding result summary
        """
        if not self.db_conn.is_local:
            return {
                'success': False,
                'error': 'Embedding requires local database with pgvector'
            }
        
        logger.info(f"Processing {len(documents)} documents")
        
        try:
            with self.db_conn.get_postgres_connection() as (conn, cur):
                # Clear existing embeddings if force=True
                if force:
                    for doc in documents:
                        cur.execute(
                            "DELETE FROM document_vectors WHERE document_id = %s", 
                            (doc['document_id'],)
                        )
                    if cur.rowcount > 0:
                        logger.info(f"Cleared {cur.rowcount} existing embeddings")
                
                # Process each document
                total_chunks = 0
                
                for doc in documents:
                    # Chunk the document
                    chunks = self.chunker.chunk_document(
                        content=doc['content'],
                        doc_id=doc['document_id'],
                        domain=doc['domain'],
                        additional_metadata={'filename': doc['filename']}
                    )
                    
                    logger.info(f"Split {doc['filename']} into {len(chunks)} chunks")
                    
                    # Generate embeddings for chunks
                    chunk_texts = [chunk.page_content for chunk in chunks]
                    chunk_embeddings = self.embeddings.embed_documents(chunk_texts)
                    
                    # Store each chunk
                    for chunk, embedding in zip(chunks, chunk_embeddings):
                        # Convert embedding to PostgreSQL array format
                        embedding_str = '[' + ','.join(map(str, embedding)) + ']'
                        
                        # Insert into database
                        # Note: When force=True, we've already deleted existing embeddings
                        # so we don't need ON CONFLICT. For safety, we'll use DO NOTHING
                        # only if there's an id conflict (primary key)
                        cur.execute("""
                            INSERT INTO document_vectors 
                            (document_id, content, metadata, embedding, 
                             domain, domain_id, created_at, updated_at)
                            VALUES (%s, %s, %s, %s::vector, %s, %s, NOW(), NOW())
                        """, (
                            doc['document_id'],
                            chunk.page_content,
                            Json(chunk.metadata),
                            embedding_str,
                            doc['domain'],
                            chunk.metadata.get('domain_id')
                        ))
                    
                    total_chunks += len(chunks)
                
                conn.commit()
                logger.info(f"✅ Embedded {total_chunks} chunks from {len(documents)} documents")
                
                return {
                    'success': True,
                    'documents_processed': len(documents),
                    'total_chunks': total_chunks,
                    'domain': documents[0]['domain'] if documents else None
                }
                
        except Exception as e:
            logger.error(f"Embedding failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'documents': len(documents)
            }
    
    def _extract_domain_from_filename(self, filename: str) -> str:
        """Extract domain from filename"""
        if '_' in filename:
            potential_domain = filename.split('_')[0]
            if '.' in potential_domain:
                return potential_domain
        return 'unknown'