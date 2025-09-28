# Copyright caerulex 2024

"""Tests for primary doc proofreader."""

from doc_proofreader.proofread_document import proofread_document
from pathlib import Path

TEST_RESOURCE_DIR = Path(Path(__file__).parent, "resources")
TEST_OUTPUTS_DIR = Path(Path(__file__).parent, "outputs")


def test_proofread_short_document():
    test_doc = Path(TEST_RESOURCE_DIR, "test_doc.docx")
    outputs = proofread_document(test_doc, save_outputs=True, save_dir=TEST_OUTPUTS_DIR)
    assert "mistake" in outputs
    assert "leafy" in outputs


def test_proofread_short_document_additional_instructions():
    test_doc = Path(TEST_RESOURCE_DIR, "test_doc.docx")
    outputs = proofread_document(
        test_doc,
        additional_instructions="'mistak' is a valid word in this document; do not correct it.",
        save_outputs=False,
    )
    assert "mistake" not in outputs
    assert "leafy" in outputs
