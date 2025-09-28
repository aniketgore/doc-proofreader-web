# Copyright caerulex 2025

"""Base client abstract class for LLM providers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(self, api_key: str, model_name: str = None):
        """Initialize the client with API key and model name."""
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    def create_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Create a chat completion and return the response text.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (overrides instance model_name)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response

        Returns:
            The response text from the model
        """
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model.

        Returns:
            Dictionary with model information including:
            - name: Model name
            - provider: Provider name
            - context_window: Maximum context size
            - cost_per_1k_tokens: Estimated cost
        """
        pass

    @abstractmethod
    def estimate_cost(self, text: str) -> float:
        """Estimate the cost for processing the given text.

        Args:
            text: The text to process

        Returns:
            Estimated cost in USD
        """
        pass

    def count_tokens(self, text: str) -> int:
        """Count approximate tokens in text.

        Simple estimation: ~4 characters per token.
        Override for more accurate model-specific counting.
        """
        return len(text) // 4