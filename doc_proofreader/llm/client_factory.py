# Copyright caerulex 2025

"""Factory for creating LLM clients."""

import os
from typing import Optional
from doc_proofreader.llm.base_client import BaseClient
from doc_proofreader.llm.openai_client import OpenAIClient
from doc_proofreader.llm.openrouter_client import OpenRouterClient


class ClientFactory:
    """Factory class for creating appropriate LLM client instances."""

    @staticmethod
    def create_client(
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> BaseClient:
        """Create and return the appropriate LLM client.

        Args:
            provider: Provider name ("openai" or "openrouter"). If None, uses env var or defaults to "openai"
            model_name: Model name. If None, uses env var or provider default
            api_key: API key. If None, uses environment variable

        Returns:
            Instance of appropriate client class

        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        # Determine provider
        if provider is None:
            provider = os.getenv("LLM_PROVIDER", "openai").lower()

        # Determine model
        if model_name is None:
            # Default to gpt-5-mini (cheap with large context)
            model_name = os.getenv("MODEL_NAME", "gpt-5-mini")

        # Get appropriate API key
        if api_key is None:
            if provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError(
                        "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
                    )
            elif provider == "openrouter":
                api_key = os.getenv("OPENROUTER_API_KEY")
                if not api_key:
                    # Fall back to OpenAI key if OpenRouter key not set
                    api_key = os.getenv("OPENAI_API_KEY")
                    if not api_key:
                        raise ValueError(
                            "OpenRouter API key not found. Please set OPENROUTER_API_KEY or OPENAI_API_KEY environment variable."
                        )
            else:
                raise ValueError(f"Unsupported provider: {provider}")

        # Create and return appropriate client
        if provider == "openai":
            return OpenAIClient(api_key=api_key, model_name=model_name)
        elif provider == "openrouter":
            return OpenRouterClient(api_key=api_key, model_name=model_name)
        else:
            raise ValueError(
                f"Unsupported provider: {provider}. Supported providers: openai, openrouter"
            )

    @staticmethod
    def get_available_models(provider: str = None) -> list:
        """Get list of available models for a provider.

        Args:
            provider: Provider name. If None, returns all models

        Returns:
            List of model names
        """
        openai_models = list(OpenAIClient.MODEL_INFO.keys())
        openrouter_models = list(OpenRouterClient.MODEL_INFO.keys())

        if provider == "openai":
            return openai_models
        elif provider == "openrouter":
            return openrouter_models
        else:
            # Return union of all models
            return sorted(list(set(openai_models + openrouter_models)))