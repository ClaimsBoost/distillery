"""
Environment configuration utilities
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from config/.env
_env_path = Path(__file__).parent.parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=_env_path)


def get_environment() -> str:
    """Get current environment (local or production)"""
    return os.getenv('ENVIRONMENT', 'local').lower()


def get_database_url() -> str:
    """Get database URL based on current environment"""
    env = get_environment()
    
    if env == 'local':
        url = os.getenv('LOCAL_DATABASE_URL')
        if not url:
            raise ValueError("LOCAL_DATABASE_URL not set in config/.env")
        return url
    else:
        # For production, use Supabase
        url = os.getenv('SUPABASE_DATABASE_URI') or os.getenv('SUPABASE_URL')
        if not url:
            raise ValueError("SUPABASE_DATABASE_URI not set in config/.env")
        return url


def get_supabase_credentials() -> tuple[str, str]:
    """Get Supabase URL and key"""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in config/.env")
    
    return url, key


def get_ollama_url() -> str:
    """Get Ollama base URL"""
    return os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')


def is_local_environment() -> bool:
    """Check if running in local environment"""
    return get_environment() == 'local'


def is_production_environment() -> bool:
    """Check if running in production environment"""
    return get_environment() == 'production'


# Convenience exports
__all__ = [
    'get_environment',
    'get_database_url',
    'get_supabase_credentials',
    'get_ollama_url',
    'is_local_environment',
    'is_production_environment'
]