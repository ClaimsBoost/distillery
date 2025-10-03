"""
Google Gemini LLM provider implementation
"""

import json
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

from .base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)

# Lazy import to avoid dependency if not using Gemini
google_genai = None


class GeminiProvider(LLMProvider):
    """Google Gemini API provider"""

    # Pricing per million tokens (as of 2025)
    PRICING = {
        "gemini-2.0-flash-exp": {"input": 0.15, "output": 0.60},
        "gemini-1.5-flash": {"input": 0.15, "output": 0.60},
        "gemini-1.5-flash-8b": {"input": 0.075, "output": 0.30},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00}
    }

    def __init__(self, settings):
        super().__init__(settings)

        # Lazy import and configure
        global google_genai
        if google_genai is None:
            try:
                import google.generativeai as genai
                google_genai = genai
            except ImportError:
                raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")

        # Configure API key
        api_key = getattr(settings.gemini, 'api_key', None) or getattr(settings.extraction, 'gemini_api_key', None)
        if not api_key:
            raise ValueError("Gemini API key not configured. Set GEMINI_API_KEY or EXTRACTION_GEMINI_API_KEY")

        google_genai.configure(api_key=api_key)

        # Get model name (allow override from settings)
        self.model_name = getattr(settings.extraction, 'gemini_model', 'gemini-1.5-flash')
        self.model = google_genai.GenerativeModel(
            self.model_name,
            generation_config={
                "response_mime_type": "application/json"
            }
        )

    def generate(self,
                 prompt: str,
                 system_prompt: Optional[str] = None,
                 schema: Optional[Dict[str, Any]] = None,
                 options: Optional[Dict[str, Any]] = None) -> Tuple[LLMResponse, Dict[str, Any]]:
        """
        Generate response using Gemini API

        Args:
            prompt: User prompt
            system_prompt: System prompt
            schema: JSON schema for structured output
            options: Gemini-specific options

        Returns:
            Tuple of (LLMResponse, request_payload)
        """
        # Build generation config
        generation_config = {
            "temperature": options.get("temperature", self.settings.extraction.temperature),
            "top_p": options.get("top_p", self.settings.extraction.top_p),
            "max_output_tokens": options.get("max_tokens", self.settings.extraction.max_tokens),
            "response_mime_type": "application/json"
        }

        # Add JSON schema if provided
        if schema:
            generation_config["response_schema"] = schema

        # Combine system prompt and user prompt
        full_prompt = []
        if system_prompt:
            full_prompt.append(f"System: {system_prompt}")
        full_prompt.append(prompt)
        combined_prompt = "\n\n".join(full_prompt)

        try:
            # Generate response
            response = self.model.generate_content(
                combined_prompt,
                generation_config=generation_config
            )

            # Extract content
            content = response.text

            # Count tokens
            input_tokens = self.count_tokens(combined_prompt)
            output_tokens = self.count_tokens(content)
            tokens_used = {
                "input": input_tokens,
                "output": output_tokens
            }

            # Calculate cost
            cost_estimate = self.estimate_cost(input_tokens, output_tokens)

            # Create LLMResponse
            llm_response = LLMResponse(
                content=content,
                tokens_used=tokens_used,
                model=self.model_name,
                provider=self.provider_name,
                raw_response={
                    "text": content,
                    "finish_reason": response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN",
                    "safety_ratings": [
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name
                        } for rating in response.candidates[0].safety_ratings
                    ] if response.candidates and response.candidates[0].safety_ratings else []
                },
                cost_estimate=cost_estimate
            )

            # Request info for storage
            request_info = {
                "model": self.model_name,
                "prompt": combined_prompt[:1000] + "..." if len(combined_prompt) > 1000 else combined_prompt,
                "temperature": generation_config["temperature"],
                "top_p": generation_config["top_p"],
                "max_tokens": generation_config["max_output_tokens"],
                "provider": self.provider_name,
                "cost_estimate": cost_estimate
            }

            return llm_response, request_info

        except Exception as e:
            logger.error(f"Gemini API request failed: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using Gemini's token counting

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        try:
            # Use Gemini's built-in token counting
            return self.model.count_tokens(text).total_tokens
        except:
            # Fallback to rough estimation
            return len(text) // 4

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: Optional[str] = None) -> float:
        """
        Estimate cost for Gemini usage

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Optional model override

        Returns:
            Estimated cost in USD
        """
        model_name = model or self.model_name

        # Get pricing for model (default to flash pricing if not found)
        pricing = self.PRICING.get(model_name, self.PRICING["gemini-1.5-flash"])

        # Calculate cost (pricing is per million tokens)
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]

        return round(input_cost + output_cost, 6)

    @property
    def provider_name(self) -> str:
        """Get provider name"""
        return "gemini"

    @property
    def supports_streaming(self) -> bool:
        """Gemini supports streaming"""
        return True

    @property
    def supports_json_schema(self) -> bool:
        """Gemini supports JSON schema validation"""
        return True