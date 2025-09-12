"""
Database connection management
Handles both local PostgreSQL and Supabase connections
"""

import logging
from typing import Optional, Dict, Any
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from supabase import create_client, Client
from src.core.settings import get_settings

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages database connections for the application"""
    
    def __init__(self):
        """Initialize database connection manager"""
        self.settings = get_settings()
        self.local_db_url = self.settings.database.local_database_uri
        self.supabase_url = self.settings.database.supabase_url
        self.supabase_key = self.settings.database.supabase_key
        
        # Determine which database to use based on environment
        self.use_local = self.settings.is_local and bool(self.local_db_url)
        self.supabase_client = None
        
        if not self.use_local:
            if self.supabase_url and self.supabase_key:
                self.supabase_client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Initialized Supabase client")
            else:
                logger.warning("No database credentials found")
    
    @property
    def is_local(self) -> bool:
        """Check if using local database"""
        return self.use_local
    
    @property
    def has_connection(self) -> bool:
        """Check if any database connection is available"""
        return bool(self.local_db_url or self.supabase_client)
    
    def get_supabase_client(self) -> Optional[Client]:
        """Get Supabase client if available"""
        return self.supabase_client
    
    @contextmanager
    def get_postgres_connection(self, cursor_factory=None):
        """
        Get PostgreSQL connection context manager
        
        Args:
            cursor_factory: Optional cursor factory (e.g., RealDictCursor)
        
        Yields:
            tuple: (connection, cursor)
        """
        if not self.local_db_url:
            raise ValueError("LOCAL_DATABASE_URL not set")
        
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(self.local_db_url)
            cur = conn.cursor(cursor_factory=cursor_factory) if cursor_factory else conn.cursor()
            yield conn, cur
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True) -> Any:
        """
        Execute a query on the local PostgreSQL database
        
        Args:
            query: SQL query to execute
            params: Query parameters
            fetch: Whether to fetch results
        
        Returns:
            Query results if fetch=True, otherwise row count
        """
        if not self.local_db_url:
            raise ValueError("LOCAL_DATABASE_URL not set")
        
        with self.get_postgres_connection() as (conn, cur):
            cur.execute(query, params)
            
            if fetch:
                return cur.fetchall()
            else:
                conn.commit()
                return cur.rowcount
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get database configuration for other components
        
        Returns:
            Configuration dictionary
        """
        return {
            'use_local': self.use_local,
            'has_supabase': bool(self.supabase_client),
            'local_db_url': self.local_db_url if self.use_local else None
        }


# Global instance for shared use
_db_connection = None

def get_database_connection() -> DatabaseConnection:
    """
    Get or create the global database connection instance
    
    Returns:
        DatabaseConnection instance
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection