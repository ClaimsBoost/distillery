"""
LLM provider factory
"""

import logging
from typing import Optional, Any

from .base import LLMProvider
from .ollama import OllamaProvider
from .gemini import GeminiProvider

logger = logging.getLogger(__name__)


def get_llm_provider(settings, provider: Optional[str] = None) -> LLMProvider:
    """
    Factory function to get appropriate LLM provider

    Args:
        settings: Application settings
        provider: Provider name override (ollama, gemini, etc.)

    Returns:
        LLMProvider instance

    Raises:
        ValueError: If provider is not supported
    """
    # Use provider from settings if not explicitly provided
    if provider is None:
        provider = getattr(settings.extraction, 'provider', 'ollama')

    provider = provider.lower()

    if provider == 'ollama':
        logger.info("Using Ollama LLM provider")
        return OllamaProvider(settings)
    elif provider == 'gemini':
        logger.info("Using Gemini LLM provider")
        return GeminiProvider(settings)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Supported: ollama, gemini")


def get_available_providers() -> list:
    """
    Get list of available providers

    Returns:
        List of provider names
    """
    providers = ['ollama']

    # Check if Gemini is available
    try:
        import google.generativeai
        providers.append('gemini')
    except ImportError:
        pass

    return providers