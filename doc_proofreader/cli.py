# Copyright caerulex 2025

"""CLI setup."""

import argparse

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
