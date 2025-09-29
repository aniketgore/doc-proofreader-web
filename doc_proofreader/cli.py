# Copyright caerulex 2025

"""CLI setup."""

import argparse
from doc_proofreader.llm.client_factory import ClientFactory

parser = argparse.ArgumentParser(
    prog="Doc-Proofreader",
    description="Proofreads documents with AI!",
    epilog="A simple app by caerulex.",
)
parser.add_argument("file_path", metavar="file-path")
parser.add_argument("--additional-instructions", type=str, default="")
parser.add_argument(
    "--inline",
    action="store_true",
    help="If True, will create a word doc with inline edits. Otherwise outputs a list of corrections for review.",
)
parser.add_argument(
    "--provider",
    type=str,
    default=None,
    choices=["openai", "openrouter"],
    help="LLM provider to use (default: uses LLM_PROVIDER env var or 'openai')",
)
parser.add_argument(
    "--model",
    type=str,
    default=None,
    help=f"Model to use for proofreading. Available models: {', '.join(ClientFactory.get_available_models())}",
)
parser.add_argument(
    "--estimate-cost",
    action="store_true",
    help="Estimate the cost before processing the document",
)
parser.add_argument(
    "--chunk",
    type=str,
    default=None,
    help="Custom chunk size: number + unit (e.g., '10000w' for 10K words, '50000c' for 50K chars, 'auto' for model-optimized)",
)
