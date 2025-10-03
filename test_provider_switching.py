#!/usr/bin/env python
"""
Test script for LLM provider switching
"""

import os
import json
from src.core.settings import get_settings
from src.llm import get_llm_provider

def test_ollama_provider():
    """Test Ollama provider"""
    print("\n=== Testing Ollama Provider ===")

    # Force Ollama provider
    os.environ['EXTRACTION_PROVIDER'] = 'ollama'
    settings = get_settings()

    provider = get_llm_provider(settings)
    print(f"Provider: {provider.provider_name}")
    print(f"Supports streaming: {provider.supports_streaming}")
    print(f"Supports JSON schema: {provider.supports_json_schema}")

    # Test generation
    try:
        prompt = "Return JSON with two fields: is_test (boolean true) and message (string 'Hello from Ollama')"
        response, request_info = provider.generate(
            prompt=prompt,
            options={"temperature": 0.1, "max_tokens": 100}
        )

        print(f"Response content: {response.content}")
        print(f"Tokens used: {response.tokens_used}")
        print(f"Cost estimate: ${response.cost_estimate:.6f}")

        # Parse JSON response
        data = json.loads(response.content)
        print(f"Parsed data: {data}")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_gemini_provider():
    """Test Gemini provider (if API key is set)"""
    print("\n=== Testing Gemini Provider ===")

    # Check if Gemini API key is set
    if not os.environ.get('GEMINI_API_KEY'):
        print("GEMINI_API_KEY not set, skipping Gemini test")
        return None

    # Force Gemini provider
    os.environ['EXTRACTION_PROVIDER'] = 'gemini'
    settings = get_settings()

    try:
        provider = get_llm_provider(settings)
        print(f"Provider: {provider.provider_name}")
        print(f"Supports streaming: {provider.supports_streaming}")
        print(f"Supports JSON schema: {provider.supports_json_schema}")

        # Test generation
        prompt = "Return JSON with two fields: is_test (boolean true) and message (string 'Hello from Gemini')"
        response, request_info = provider.generate(
            prompt=prompt,
            options={"temperature": 0.1, "max_tokens": 100}
        )

        print(f"Response content: {response.content}")
        print(f"Tokens used: {response.tokens_used}")
        print(f"Cost estimate: ${response.cost_estimate:.6f}")

        # Parse JSON response
        data = json.loads(response.content)
        print(f"Parsed data: {data}")

        return True
    except ImportError as e:
        print(f"Import error (google-generativeai not installed): {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_extraction_with_provider():
    """Test extraction with current provider"""
    print("\n=== Testing Extraction with Current Provider ===")

    from src.commands.extract_command import ExtractCommand

    # Create extract command
    cmd = ExtractCommand()

    # Access provider through one of the extractors
    extractor = cmd.extractors.get('law_firm_confirmation')
    if extractor:
        print(f"Current provider: {extractor.provider.provider_name}")
        print(f"Provider initialized: {extractor.provider is not None}")
        print(f"Provider type: {type(extractor.provider).__name__}")
        return True
    else:
        print("Could not access extractor")
        return False


if __name__ == "__main__":
    print("Testing LLM Provider Switching")
    print("=" * 50)

    # Test Ollama
    ollama_success = test_ollama_provider()

    # Test Gemini (if available)
    gemini_success = test_gemini_provider()

    # Test extraction integration
    extraction_success = test_extraction_with_provider()

    # Summary
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"  Ollama: {'✓ Passed' if ollama_success else '✗ Failed'}")
    print(f"  Gemini: {'✓ Passed' if gemini_success else '- Skipped' if gemini_success is None else '✗ Failed'}")
    print(f"  Extraction: {'✓ Passed' if extraction_success else '✗ Failed'}")