# Copyright caerulex 2025

"""Chunk size utilities and optimization."""

import re
from typing import Dict, Tuple


def parse_chunk_size(chunk_arg: str) -> int:
    """Parse chunk size argument into character count.

    Args:
        chunk_arg: String like '10000w', '50000c', or 'auto'

    Returns:
        Character count for chunking

    Examples:
        '5000w' -> 27500 (5000 words * 5.5 chars/word)
        '30000c' -> 30000 (30000 characters)
        'auto' -> 0 (will be calculated based on model)
    """
    if chunk_arg.lower() == 'auto':
        return 0  # Signal for auto-calculation

    # Parse pattern like '5000w' or '30000c'
    match = re.match(r'^(\d+)([wc])$', chunk_arg.lower())
    if not match:
        raise ValueError(
            f"Invalid chunk format: '{chunk_arg}'. "
            "Use format like '5000w' (words) or '30000c' (characters) or 'auto'"
        )

    number, unit = match.groups()
    number = int(number)

    if unit == 'w':  # words
        # Convert words to characters (average 5.5 chars per word)
        return int(number * 5.5)
    elif unit == 'c':  # characters
        return number
    else:
        raise ValueError(f"Unknown unit: {unit}. Use 'w' for words or 'c' for characters")


def get_optimal_chunk_size(model_name: str, context_window: int) -> int:
    """Calculate optimal chunk size based on model capabilities.

    Args:
        model_name: Name of the model
        context_window: Model's context window in tokens

    Returns:
        Optimal chunk size in characters
    """
    # Conservative usage of context window (leaving room for prompts + output)
    usable_tokens = int(context_window * 0.3)  # Use 30% of context (more conservative)

    # Convert tokens to characters (4 chars per token average)
    calculated_chars = usable_tokens * 4

    # Model-specific optimizations with reasonable limits
    if 'gemini-2.5' in model_name:
        # Gemini 2.5 Pro - large but manageable chunks
        return min(calculated_chars, 80000)   # Max 80K chars (~14K words)
    elif 'gemini' in model_name:
        # Other Gemini models
        return min(calculated_chars, 60000)   # Max 60K chars (~11K words)
    elif 'claude' in model_name:
        # Claude models
        return min(calculated_chars, 50000)   # Max 50K chars (~9K words)
    elif 'gpt-5' in model_name:
        # GPT-5 family (large context)
        return min(calculated_chars, 70000)   # Max 70K chars (~12K words)
    elif 'gpt-4o' in model_name:
        # GPT-4o
        return min(calculated_chars, 40000)   # Max 40K chars (~7K words)
    elif 'gpt-4' in model_name:
        # GPT-4 (smaller context)
        return min(calculated_chars, 20000)   # Max 20K chars (~3.6K words)
    else:
        # Conservative default
        return min(calculated_chars, 30000)   # Max 30K chars (~5.5K words)


def get_chunk_recommendations(model_name: str, context_window: int) -> Dict[str, str]:
    """Get chunk size recommendations for different use cases.

    Returns:
        Dictionary with recommended chunk sizes and descriptions
    """
    optimal = get_optimal_chunk_size(model_name, context_window)

    return {
        'auto': f'{optimal}c (model-optimized)',
        'small': '15000c (~2.7K words - safe for all models)',
        'medium': '55000c (~10K words - good balance)',
        'large': f'{optimal}c (~{optimal//5.5:.0f} words - max for {model_name})',
        'words_small': '3000w (~16.5K chars)',
        'words_medium': '10000w (~55K chars)',
        'words_large': f'{optimal//5.5:.0f}w (~{optimal}chars)',
    }


def validate_chunk_size(chunk_size: int, model_name: str, context_window: int) -> Tuple[bool, str]:
    """Validate if chunk size is appropriate for the model.

    Returns:
        (is_valid, warning_message)
    """
    optimal = get_optimal_chunk_size(model_name, context_window)

    if chunk_size <= 1000:
        return False, f"Chunk size too small ({chunk_size} chars). Minimum recommended: 5000c"

    if chunk_size > optimal * 1.5:
        return False, f"Chunk size too large ({chunk_size} chars). Maximum for {model_name}: {optimal}c"

    if chunk_size > optimal:
        return True, f"⚠️  Large chunk size ({chunk_size} chars). Optimal for {model_name}: {optimal}c"

    return True, ""  # Valid size, no warning