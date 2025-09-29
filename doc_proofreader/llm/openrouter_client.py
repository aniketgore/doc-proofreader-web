# Copyright caerulex 2025

"""OpenRouter client implementation."""

from typing import List, Dict, Any, Optional
from openai import OpenAI
from doc_proofreader.llm.base_client import BaseClient


class OpenRouterClient(BaseClient):
    """OpenRouter API client implementation using OpenAI-compatible interface."""

    # Model mappings and pricing (as of 2025)
    MODEL_INFO = {
        "gpt-5-mini": {
            "openrouter_name": "openai/gpt-5-mini",
            "context_window": 400000,
            "cost_per_1k_input": 0.0001,
            "cost_per_1k_output": 0.0004,
        },
        "gemini-2.5-pro": {
            "openrouter_name": "google/gemini-2.5-pro",
            "context_window": 1000000,
            "cost_per_1k_input": 0.00125,
            "cost_per_1k_output": 0.005,
        },
        "gpt-4o": {
            "openrouter_name": "openai/gpt-4o",
            "context_window": 128000,
            "cost_per_1k_input": 0.0025,
            "cost_per_1k_output": 0.01,
        },
        "gpt-4o-mini": {
            "openrouter_name": "openai/gpt-4o-mini",
            "context_window": 128000,
            "cost_per_1k_input": 0.00015,
            "cost_per_1k_output": 0.0006,
        },
        "claude-3.5-sonnet": {
            "openrouter_name": "anthropic/claude-3.5-sonnet",
            "context_window": 200000,
            "cost_per_1k_input": 0.003,
            "cost_per_1k_output": 0.015,
        },
        "claude-3-opus": {
            "openrouter_name": "anthropic/claude-3-opus",
            "context_window": 200000,
            "cost_per_1k_input": 0.015,
            "cost_per_1k_output": 0.075,
        },
        "claude-3-haiku": {
            "openrouter_name": "anthropic/claude-3-haiku",
            "context_window": 200000,
            "cost_per_1k_input": 0.00025,
            "cost_per_1k_output": 0.00125,
        },
        "gemini-1.5-pro": {
            "openrouter_name": "google/gemini-pro-1.5",
            "context_window": 1000000,
            "cost_per_1k_input": 0.00125,
            "cost_per_1k_output": 0.005,
        },
        "gemini-1.5-flash": {
            "openrouter_name": "google/gemini-flash-1.5",
            "context_window": 1000000,
            "cost_per_1k_input": 0.00025,
            "cost_per_1k_output": 0.00125,
        },
        "llama-3.1-70b": {
            "openrouter_name": "meta-llama/llama-3.1-70b-instruct",
            "context_window": 131072,
            "cost_per_1k_input": 0.00059,
            "cost_per_1k_output": 0.00079,
        },
        "mixtral-8x7b": {
            "openrouter_name": "mistralai/mixtral-8x7b-instruct",
            "context_window": 32768,
            "cost_per_1k_input": 0.00024,
            "cost_per_1k_output": 0.00024,
        },
    }

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-pro",
        site_url: str = "https://github.com/caerulex/doc-proofreader",
        app_name: str = "Doc-Proofreader",
    ):
        """Initialize OpenRouter client.

        Args:
            api_key: OpenRouter API key
            model_name: Simplified model name (e.g., "gpt-4o", "claude-3.5-sonnet")
            site_url: Your site URL (for OpenRouter HTTP-Referer header)
            app_name: Application name (for OpenRouter X-Title header)
        """
        super().__init__(api_key, model_name)

        # Get the OpenRouter-specific model name
        model_info = self.MODEL_INFO.get(model_name)
        if not model_info:
            raise ValueError(
                f"Model '{model_name}' not supported. "
                f"Available models: {', '.join(self.MODEL_INFO.keys())}"
            )

        self.openrouter_model_name = model_info["openrouter_name"]

        # Store site info for headers
        self.site_url = site_url
        self.app_name = app_name

        # Create OpenAI client with OpenRouter base URL
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def create_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Create a chat completion using OpenRouter API."""
        if model:
            # Convert simplified name to OpenRouter format
            model_info = self.MODEL_INFO.get(model)
            if model_info:
                model_to_use = model_info["openrouter_name"]
            else:
                # Assume it's already in OpenRouter format
                model_to_use = model
        else:
            model_to_use = self.openrouter_model_name

        kwargs = {
            "model": model_to_use,
            "messages": messages,
            "temperature": temperature,
            "extra_headers": {
                "HTTP-Referer": self.site_url,
                "X-Title": self.app_name,
            },
        }
        if max_tokens:
            kwargs["max_tokens"] = max_tokens

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content.strip()

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        model_data = self.MODEL_INFO.get(self.model_name)
        if not model_data:
            # Return default info if model not in our list
            return {
                "name": self.model_name,
                "provider": "openrouter",
                "context_window": 128000,
                "cost_per_1k_input": 0.001,
                "cost_per_1k_output": 0.001,
            }

        return {
            "name": self.model_name,
            "provider": "openrouter",
            "openrouter_name": model_data["openrouter_name"],
            "context_window": model_data["context_window"],
            "cost_per_1k_input": model_data["cost_per_1k_input"],
            "cost_per_1k_output": model_data["cost_per_1k_output"],
        }

    def estimate_cost(self, text: str) -> float:
        """Estimate cost for processing text."""
        model_info = self.get_model_info()
        tokens = self.count_tokens(text)

        # Estimate assuming 50% of tokens for output
        input_cost = (tokens / 1000) * model_info["cost_per_1k_input"]
        output_cost = (tokens * 0.5 / 1000) * model_info["cost_per_1k_output"]

        return input_cost + output_cost