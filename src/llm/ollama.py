"""
Ollama LLM provider implementation
"""

import json
import logging
from typing import Dict, Any, Optional, Tuple
import requests
from datetime import datetime

from .base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    """Ollama API provider"""

    def __init__(self, settings):
        super().__init__(settings)
        self.base_url = settings.ollama.base_url
        self.model = settings.extraction.ollama_model
        if not self.model:
            raise ValueError("EXTRACTION_OLLAMA_MODEL must be set when using Ollama provider")

    def generate(self,
                 prompt: str,
                 system_prompt: Optional[str] = None,
                 schema: Optional[Dict[str, Any]] = None,
                 options: Optional[Dict[str, Any]] = None) -> Tuple[LLMResponse, Dict[str, Any]]:
        """
        Generate response using Ollama API

        Args:
            prompt: User prompt
            system_prompt: System prompt
            schema: JSON schema for structured output
            options: Ollama-specific options

        Returns:
            Tuple of (LLMResponse, request_payload)
        """
        url = f"{self.base_url}/api/generate"

        # Build options with defaults from settings
        ollama_options = {
            "temperature": self.settings.extraction.temperature,
            "top_p": self.settings.extraction.top_p,
            "seed": self.settings.ollama.extraction_seed,
            "num_ctx": self.settings.ollama.num_ctx,
            "num_predict": options.get("max_tokens")  # Must be provided by caller
        }

        # Override with provided options
        if options:
            ollama_options.update({k: v for k, v in options.items() if k != "max_tokens"})

        # Build payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt or "",
            "format": schema if schema else "json",
            "options": ollama_options,
            "stream": False,
            "keep_alive": 0  # Reset context after each request
        }

        # Add timestamp
        payload['_request_timestamp'] = datetime.now().isoformat()

        logger.debug(f"Calling Ollama API with model={self.model}, num_predict={ollama_options.get('num_predict')}")

        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            response_data = response.json()

            # Extract token counts (Ollama provides these in the response)
            tokens_used = {
                "input": response_data.get("prompt_eval_count", 0),
                "output": response_data.get("eval_count", 0)
            }

            # Create LLMResponse
            llm_response = LLMResponse(
                content=response_data.get("response", ""),
                tokens_used=tokens_used,
                model=self.model,
                provider=self.provider_name,
                raw_response=response_data,
                cost_estimate=0.0  # Ollama is free (local)
            )

            # Return response and request payload (for storage)
            request_info = {
                "model": self.model,
                "prompt": prompt[:1000] + "..." if len(prompt) > 1000 else prompt,
                "temperature": ollama_options["temperature"],
                "top_p": ollama_options["top_p"],
                "max_tokens": ollama_options["num_predict"],
                "provider": self.provider_name
            }

            return llm_response, request_info

        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API request failed: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Ollama response: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text

        Args:
            text: Text to count tokens for

        Returns:
            Estimated number of tokens
        """
        # Rough estimation: 1 token ≈ 4 characters
        return len(text) // 4

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: Optional[str] = None) -> float:
        """
        Estimate cost for Ollama (always 0 since it's local)

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Optional model override

        Returns:
            0.0 (Ollama is free)
        """
        return 0.0

    @property
    def provider_name(self) -> str:
        """Get provider name"""
        return "ollama"

    @property
    def supports_streaming(self) -> bool:
        """Ollama supports streaming"""
        return True

    @property
    def supports_json_schema(self) -> bool:
        """Ollama supports JSON schema via format parameter"""
        return True