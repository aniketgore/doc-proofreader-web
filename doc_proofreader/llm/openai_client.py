# Copyright caerulex 2025

"""OpenAI client implementation."""

from typing import List, Dict, Any, Optional
from openai import OpenAI
from doc_proofreader.llm.base_client import BaseClient


class OpenAIClient(BaseClient):
    """OpenAI API client implementation."""

    # Model information and pricing (as of 2025)
    MODEL_INFO = {
        "gpt-5-mini": {
            "context_window": 400000,
            "cost_per_1k_input": 0.0001,
            "cost_per_1k_output": 0.0004,
        },
        "gpt-4o": {
            "context_window": 128000,
            "cost_per_1k_input": 0.0025,
            "cost_per_1k_output": 0.01,
        },
        "gpt-4o-mini": {
            "context_window": 128000,
            "cost_per_1k_input": 0.00015,
            "cost_per_1k_output": 0.0006,
        },
        "gpt-4": {
            "context_window": 8192,
            "cost_per_1k_input": 0.03,
            "cost_per_1k_output": 0.06,
        },
        "gpt-3.5-turbo": {
            "context_window": 16385,
            "cost_per_1k_input": 0.0005,
            "cost_per_1k_output": 0.0015,
        },
    }

    def __init__(self, api_key: str, model_name: str = "gpt-4o"):
        """Initialize OpenAI client."""
        super().__init__(api_key, model_name)
        self.client = OpenAI(api_key=api_key)

    def create_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Create a chat completion using OpenAI API."""
        model_to_use = model or self.model_name

        kwargs = {
            "model": model_to_use,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            kwargs["max_tokens"] = max_tokens

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content.strip()

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        model_data = self.MODEL_INFO.get(self.model_name, self.MODEL_INFO["gpt-4o"])

        return {
            "name": self.model_name,
            "provider": "openai",
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