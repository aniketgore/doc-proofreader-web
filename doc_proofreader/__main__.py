# Copyright caerulex 2025

"""Main entrypoint of doc-proofreader."""

from doc_proofreader.proofread_document import proofread_document
from doc_proofreader.proofread_document_inline import (
    proofread_document_with_track_changes_mac,
)
from doc_proofreader.cli import parser
from pathlib import Path

OUTPUT_DIR = Path(Path(__file__).parent.parent, "proofread_files")

if __name__ == "__main__":
    args = parser.parse_args()
    print("Processing ", args.file_path, args.inline, args.additional_instructions)
    if args.inline:
        print("Editing document inline...")
        proofread_document_with_track_changes_mac(
            args.file_path, args.additional_instructions, save_dir=OUTPUT_DIR
        )
    else:
        print("Editing document...")
        proofread_document(
            args.file_path, args.additional_instructions, save_dir=OUTPUT_DIR
        )
