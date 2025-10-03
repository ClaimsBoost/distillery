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

        # Get model name from settings
        self.model_name = settings.extraction.gemini_model
        self.model = google_genai.GenerativeModel(
            self.model_name,
            generation_config={
                "response_mime_type": "application/json"
            }
        )

    def _convert_schema_for_gemini(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert JSON Schema to Gemini-compatible format

        Args:
            schema: JSON Schema dictionary

        Returns:
            Gemini-compatible schema
        """
        if not schema:
            return schema

        result = {}

        for key, value in schema.items():
            # Skip $schema field
            if key == "$schema":
                continue

            # Handle type field with array notation
            if key == "type" and isinstance(value, list):
                # Convert ["string", "null"] to string with nullable
                non_null_types = [t for t in value if t != "null"]
                if "null" in value:
                    result["nullable"] = True
                if len(non_null_types) == 1:
                    result["type"] = non_null_types[0]
                else:
                    # Multiple non-null types not supported by Gemini
                    result["type"] = non_null_types[0]
            # Recursively process nested schemas
            elif key == "properties" and isinstance(value, dict):
                result["properties"] = {
                    prop_name: self._convert_schema_for_gemini(prop_value)
                    for prop_name, prop_value in value.items()
                }
            elif key == "items" and isinstance(value, dict):
                result["items"] = self._convert_schema_for_gemini(value)
            # Keep description but Gemini ignores it
            elif key == "description":
                continue  # Skip descriptions as Gemini doesn't use them
            else:
                result[key] = value

        return result

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
            "response_mime_type": "application/json"
        }

        # Only add max_output_tokens if provided (let Gemini use its default otherwise)
        if options.get("max_tokens"):
            generation_config["max_output_tokens"] = options["max_tokens"]

        # Add JSON schema if provided
        if schema:
            # Convert JSON Schema to Gemini-compatible format
            gemini_schema = self._convert_schema_for_gemini(schema)
            generation_config["response_schema"] = gemini_schema

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

            # Extract content - handle different response formats
            try:
                # Try the simple text accessor first
                content = response.text
            except Exception as e:
                # Fall back to manual extraction from candidates
                if response.candidates and len(response.candidates) > 0:
                    # Try to get text from the first candidate
                    candidate = response.candidates[0]

                    # Check finish reason
                    finish_reason_name = candidate.finish_reason.name if hasattr(candidate.finish_reason, 'name') else str(candidate.finish_reason)

                    if finish_reason_name == "MAX_TOKENS" or candidate.finish_reason == 4:
                        # Hit max tokens limit - try to get partial content
                        if candidate.content and candidate.content.parts and len(candidate.content.parts) > 0:
                            content = candidate.content.parts[0].text
                            logger.warning(f"Gemini hit max_tokens limit, returning partial response")
                        else:
                            # No partial content available, return empty JSON structure
                            logger.warning(f"Gemini hit max_tokens with no partial content, returning empty structure")
                            content = "{}"
                    elif candidate.content and candidate.content.parts:
                        content = candidate.content.parts[0].text
                    else:
                        logger.error(f"No content in candidate: finish_reason={finish_reason_name}")
                        raise ValueError(f"Gemini returned no content (finish_reason={finish_reason_name})")
                else:
                    raise ValueError("Gemini returned no valid response")

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
                "max_tokens": generation_config.get("max_output_tokens", "default"),
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