"""
Vector store implementations for document embeddings
Supports both local PostgreSQL with pgvector and Supabase
"""

import logging
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain.schema import Document
from langchain_community.vectorstores import SupabaseVectorStore
from src.core.settings import get_settings

logger = logging.getLogger(__name__)


class BaseVectorStore(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    def similarity_search(self, query: str, k: int = 5, filter: Optional[Dict] = None) -> List[Document]:
        """Search for similar documents"""
        pass
    
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the store"""
        pass


class LocalPGVectorStore(BaseVectorStore):
    """PostgreSQL pgvector store for local development"""
    
    def __init__(self, connection_string: str, embeddings):
        """
        Initialize local PostgreSQL vector store
        
        Args:
            connection_string: PostgreSQL connection string
            embeddings: Embeddings model instance
        """
        self.conn_string = connection_string
        self.embeddings = embeddings
        logger.info("Initialized LocalPGVectorStore")
    
    def similarity_search(self, query: str, k: int = 5, filter: Optional[Dict] = None) -> List[Document]:
        """
        Perform similarity search

        Args:
            query: Query text
            k: Number of results to return
            filter: Optional filter dict with 'domain_id' or 'document_id'

        Returns:
            List of similar documents
        """
        # Generate embedding for query
        query_embedding = self.embeddings.embed_query(query)
        # Convert to numpy array for proper pgvector handling
        query_embedding = np.array(query_embedding)

        # Connect to database
        conn = psycopg2.connect(self.conn_string)
        # Register vector type for this connection
        register_vector(conn)
        cur = conn.cursor()

        try:
            # WORKAROUND: PostgreSQL query planner issue with pgvector
            # When using WHERE + ORDER BY <=> + small LIMIT, the planner may choose
            # an inefficient index scan that returns 0 results.
            # Solution: Fetch more results than needed (min 100) and limit in Python
            fetch_limit = max(k * 10, 100)

            # Build SQL query with filter
            if filter and 'domain_id' in filter:
                sql = """
                SELECT id, content, metadata, embedding <=> %s as distance
                FROM document_vectors
                WHERE domain_id = %s
                ORDER BY distance
                LIMIT %s
                """
                cur.execute(sql, (query_embedding, filter['domain_id'], fetch_limit))
            elif filter and 'document_id' in filter:
                sql = """
                SELECT id, content, metadata, embedding <=> %s as distance
                FROM document_vectors
                WHERE document_id = %s
                ORDER BY distance
                LIMIT %s
                """
                cur.execute(sql, (query_embedding, filter['document_id'], fetch_limit))
            else:
                sql = """
                SELECT id, content, metadata, embedding <=> %s as distance
                FROM document_vectors
                ORDER BY distance
                LIMIT %s
                """
                cur.execute(sql, (query_embedding, fetch_limit))

            results = cur.fetchall()
            docs = []
            # Only take the first k results
            for row in results[:k]:
                metadata = row[2] or {}
                metadata['id'] = str(row[0])  # Add the ID to metadata
                docs.append(Document(page_content=row[1], metadata=metadata))
            return docs

        finally:
            cur.close()
            conn.close()
    
    def similarity_search_with_metadata_boost(self, query: str, k: int = 5,
                                            filter: Optional[Dict] = None,
                                            boost_field: Optional[str] = None) -> List[Document]:
        """
        Search with metadata boosting for better retrieval

        Args:
            query: Query text
            k: Number of results
            filter: Optional filter
            boost_field: Metadata field to boost (e.g., 'contains_addresses', 'contains_money', 'contains_emails', 'contains_phone_numbers')

        Returns:
            List of documents sorted by boost field then similarity
        """
        # Generate embedding for query
        query_embedding = self.embeddings.embed_query(query)
        # Convert to numpy array for proper pgvector handling
        query_embedding = np.array(query_embedding)

        # Connect to database
        conn = psycopg2.connect(self.conn_string)
        # Register vector type for this connection
        register_vector(conn)
        cur = conn.cursor()

        try:
            # Map boost fields to their count fields
            boost_field_mapping = {
                'contains_addresses': 'address_count',
                'contains_money': 'money_count',
                'contains_emails': 'email_count',
                'contains_phone_numbers': 'phone_count',
                'contains_contact': 'contact_count'  # Combined emails + phones
            }

            # If boost field is specified and we have a mapping for it
            if boost_field and boost_field in boost_field_mapping:
                count_field = boost_field_mapping[boost_field]

                # WORKAROUND: Same query planner issue - fetch more and limit in Python
                fetch_limit = max(k * 10, 100)

                # Build SQL with dynamic field names
                order_clause = f"""
                    CASE WHEN metadata->>'{boost_field}' = 'true' THEN 0 ELSE 1 END,
                    CAST(COALESCE(metadata->>'{count_field}', '0') AS INTEGER) DESC,
                    embedding <=> %s::vector
                """

                if filter and 'domain_id' in filter:
                    sql = f"""
                    SELECT id, content, metadata, embedding <=> %s::vector as distance
                    FROM document_vectors
                    WHERE domain_id = %s
                    ORDER BY {order_clause}
                    LIMIT %s
                    """
                    cur.execute(sql, (query_embedding, filter['domain_id'], query_embedding, fetch_limit))
                elif filter and 'document_id' in filter:
                    sql = f"""
                    SELECT id, content, metadata, embedding <=> %s::vector as distance
                    FROM document_vectors
                    WHERE document_id = %s
                    ORDER BY {order_clause}
                    LIMIT %s
                    """
                    cur.execute(sql, (query_embedding, filter['document_id'], query_embedding, fetch_limit))
                else:
                    sql = f"""
                    SELECT id, content, metadata, embedding <=> %s::vector as distance
                    FROM document_vectors
                    ORDER BY {order_clause}
                    LIMIT %s
                    """
                    cur.execute(sql, (query_embedding, query_embedding, fetch_limit))

                results = cur.fetchall()
                docs = []
                # Only take the first k results (workaround for query planner issue)
                for row in results[:k]:
                    metadata = row[2] or {}
                    metadata['id'] = str(row[0])  # Add the ID to metadata
                    docs.append(Document(page_content=row[1], metadata=metadata))

                # Log what we retrieved
                logger.info(f"Retrieved {len(docs)} chunks with {boost_field} boosting")
                for i, doc in enumerate(docs[:3]):
                    meta = doc.metadata
                    logger.debug(f"Chunk {i}: {boost_field}={meta.get(boost_field)}, {count_field}={meta.get(count_field)}")

                return docs

            # For other boost fields or no boost, use regular search
            else:
                return self.similarity_search(query, k, filter)

        finally:
            cur.close()
            conn.close()
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to vector store (not implemented for local store)
        Documents should be added via DocumentEmbedder
        """
        raise NotImplementedError("Use DocumentEmbedder to add documents to local store")


class SupabaseVectorStoreWrapper(BaseVectorStore):
    """Wrapper around LangChain's SupabaseVectorStore for consistency"""

    def __init__(self, client, embeddings, table_name: str = "document_vectors"):
        """
        Initialize Supabase vector store wrapper

        Args:
            client: Supabase client
            embeddings: Embeddings model
            table_name: Table name for vectors
        """
        self.client = client
        self.embeddings = embeddings
        self.table_name = table_name
        self.store = SupabaseVectorStore(
            client=client,
            embedding=embeddings,
            table_name=table_name,
            query_name="match_documents"
        )
        logger.info("Initialized SupabaseVectorStore")

    def similarity_search(self, query: str, k: int = 5, filter: Optional[Dict] = None) -> List[Document]:
        """Perform similarity search"""
        return self.store.similarity_search(query, k=k, filter=filter)

    def similarity_search_with_metadata_boost(self, query: str, k: int = 5,
                                            filter: Optional[Dict] = None,
                                            boost_field: Optional[str] = None) -> List[Document]:
        """
        Search with metadata boosting for better retrieval (Supabase version)

        Args:
            query: Query text
            k: Number of results
            filter: Optional filter
            boost_field: Metadata field to boost (e.g., 'contains_addresses', 'contains_money', 'contains_emails', 'contains_phone_numbers')

        Returns:
            List of documents sorted by boost field then similarity
        """
        # Map boost fields to their count fields
        boost_field_mapping = {
            'contains_addresses': 'address_count',
            'contains_money': 'money_count',
            'contains_emails': 'email_count',
            'contains_phone_numbers': 'phone_count',
            'contains_contact': 'contact_count'  # Combined emails + phones
        }

        # If boost field is specified and we have a mapping for it
        if boost_field and boost_field in boost_field_mapping:
            count_field = boost_field_mapping[boost_field]

            # Generate embedding for query
            query_embedding = self.embeddings.embed_query(query)

            # Build the RPC query with metadata boosting
            # Note: This assumes you have a custom RPC function in Supabase
            # For now, we'll fall back to regular search with a warning
            logger.warning(f"Supabase metadata boost for {boost_field} not yet implemented - using regular search")
            return self.similarity_search(query, k, filter)
        else:
            # For no boost field, use regular search
            return self.similarity_search(query, k, filter)

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to store"""
        self.store.add_documents(documents)


def create_vector_store(config: Dict[str, Any], embeddings, supabase_client=None) -> BaseVectorStore:
    """
    Factory function to create appropriate vector store
    
    Args:
        config: Configuration dictionary
        embeddings: Embeddings model instance
        supabase_client: Optional Supabase client
    
    Returns:
        Vector store instance
    """
    # Get settings
    settings = get_settings()
    local_db_url = settings.database.local_database_uri
    
    if settings.is_local and local_db_url:
        logger.info("Using LocalPGVectorStore with local PostgreSQL")
        return LocalPGVectorStore(local_db_url, embeddings)
    elif supabase_client:
        logger.info("Using SupabaseVectorStore")
        return SupabaseVectorStoreWrapper(supabase_client, embeddings)
    else:
        raise ValueError("No database configuration found. Set LOCAL_DATABASE_URI or provide Supabase client.")