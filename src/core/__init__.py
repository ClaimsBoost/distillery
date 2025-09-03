"""Core components and configuration"""
from .config_manager import ExtractionConfig, ModelType
from .prompts import PromptTemplates
from .env_config import (
    get_environment,
    get_database_url,
    get_supabase_credentials,
    get_ollama_url,
    is_local_environment,
    is_production_environment
)

__all__ = [
    'ExtractionConfig',
    'ModelType',
    'PromptTemplates',
    'get_environment',
    'get_database_url',
    'get_supabase_credentials',
    'get_ollama_url',
    'is_local_environment',
    'is_production_environment'
]