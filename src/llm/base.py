"""
Base LLM provider interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LLMResponse:
    """Standard response from LLM providers"""
    content: str
    tokens_used: Dict[str, int]  # {"input": N, "output": M}
    model: str
    provider: str
    raw_response: Dict[str, Any]
    cost_estimate: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "content": self.content,
            "tokens_used": self.tokens_used,
            "model": self.model,
            "provider": self.provider,
            "cost_estimate": self.cost_estimate,
            "_timestamp": datetime.now().isoformat()
        }


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, settings):
        """
        Initialize provider with settings

        Args:
            settings: Application settings object
        """
        self.settings = settings

    @abstractmethod
    def generate(self,
                 prompt: str,
                 system_prompt: Optional[str] = None,
                 schema: Optional[Dict[str, Any]] = None,
                 options: Optional[Dict[str, Any]] = None) -> Tuple[LLMResponse, Dict[str, Any]]:
        """
        Generate a response from the LLM

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            schema: Optional JSON schema for structured output
            options: Provider-specific options (temperature, max_tokens, etc.)

        Returns:
            Tuple of (LLMResponse, request_payload)
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        pass

    @abstractmethod
    def estimate_cost(self, input_tokens: int, output_tokens: int, model: Optional[str] = None) -> float:
        """
        Estimate cost for token usage

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Optional model override

        Returns:
            Estimated cost in USD
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get provider name"""
        pass

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """Check if provider supports streaming"""
        pass

    @property
    @abstractmethod
    def supports_json_schema(self) -> bool:
        """Check if provider supports JSON schema validation"""
        pass