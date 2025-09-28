# Copyright caerulex 2025

"""Mac-compatible doc-proofreader with inline track changes using AppleScript."""

from openai import OpenAI
from datetime import datetime
from docx import Document
from pathlib import Path
from dotenv import load_dotenv
import os
import sys
import subprocess
from doc_proofreader.prompts.system_prompts import DIRECT_EDIT_SYSTEM_PROMPT

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=API_KEY)
SUPPORTED_OS = ["darwin"]


def clear_all_paragraphs(document):
    """
    Clears all paragraphs from a python-docx Document object.
    """
    # Iterate through paragraphs in reverse order to avoid issues with index shifts
    for paragraph in reversed(document.paragraphs):
        p = paragraph._element
        p.getparent().remove(p)
        # Clear the internal references to the deleted paragraph
        paragraph._p = paragraph._element = None


def process_chunk_for_direct_edit(chunk: str, additional_instructions: str):
    """Process chunk and return corrected text directly."""
    print("Processing chunk for direct edit...")

    messages = [
        {"role": "system", "content": DIRECT_EDIT_SYSTEM_PROMPT},
        {"role": "user", "content": chunk},
    ]

    if additional_instructions:
        messages.insert(
            1,
            {
                "role": "user",
                "content": f"Additional instructions: {additional_instructions}",
            },
        )

    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        temperature=0.1,
    )

    return response.choices[0].message.content.strip()


def create_corrected_document_from_chunks(
    original_doc_path, original_chunks, corrected_chunks
):
    """Create a new document with corrections applied, preserving formatting."""
    original_doc = Document(original_doc_path)
    corrected_doc = Document(original_doc_path)
    clear_all_paragraphs(corrected_doc)

    # Process paragraphs
    para_idx = 0
    for chunk_idx, (original_chunk, corrected_chunk) in enumerate(
        zip(original_chunks, corrected_chunks)
    ):
        corrected_lines = corrected_chunk.split("  \n")

        for line_idx, corrected_line in enumerate(corrected_lines):
            if corrected_line.strip():  # Skip empty lines
                if para_idx < len(original_doc.paragraphs):
                    original_para = original_doc.paragraphs[para_idx]
                    new_para = corrected_doc.add_paragraph()

                    # Copy paragraph style
                    try:
                        print(f"Copied para style to be {original_para.style}")
                        new_para.style = original_para.style
                    except Exception as e:
                        print(f"Couldn't copy para style -- {e}")

                    # Parse and apply formatting
                    apply_formatted_text_to_paragraph(new_para, corrected_line)
                    para_idx += 1
                else:
                    # Add any remaining paragraphs
                    new_para = corrected_doc.add_paragraph()
                    apply_formatted_text_to_paragraph(new_para, corrected_line)

    return corrected_doc


def apply_formatted_text_to_paragraph(paragraph, formatted_text):
    """Apply formatted text with HTML-like tags to a paragraph."""
    import re

    # Clear existing runs
    paragraph.clear()

    # Pattern to match formatting tags and text
    pattern = r"(<b><i>|<b>|<i>|</b></i>|</b>|</i>)"
    parts = re.split(pattern, formatted_text)

    current_bold = False
    current_italic = False

    for part in parts:
        if part == "<b>":
            current_bold = True
        elif part == "</b>":
            current_bold = False
        elif part == "<i>":
            current_italic = True
        elif part == "</i>":
            current_italic = False
        elif part == "<b><i>":
            current_bold = True
            current_italic = True
        elif part == "</b></i>" or part == "</i></b>":
            current_bold = False
            current_italic = False
        elif part and part not in ["<b><i>", "<b>", "<i>", "</b></i>", "</b>", "</i>"]:
            # This is actual text
            if part.strip():
                run = paragraph.add_run(part)
                run.bold = current_bold
                run.italic = current_italic


def compare_documents_with_applescript(original_path, corrected_path) -> None:
    """Execute AppleScript in a single comprehensive block to avoid variable scoping issues."""

    # Convert to absolute paths
    original_abs = str(Path(original_path).resolve())
    corrected_abs = str(Path(corrected_path).resolve())

    print(f"🔍 Original document: {original_abs}")
    print(f"🔍 Corrected document: {corrected_abs}")

    # Single comprehensive AppleScript that does everything in one block
    comprehensive_script = f"""set old to "{original_abs}"
set new to "{corrected_abs}"
tell application "Microsoft Word"
    activate
    open old
    compare active document path new as text
end tell
"""

    try:
        # Execute the comprehensive script
        subprocess.run(
            ["osascript", "-e", comprehensive_script],
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        print("❌ AppleScript execution timed out")
        return False
    except Exception as e:
        print(f"❌ Error executing AppleScript: {e}")
        return False


def proofread_document_with_track_changes_mac(
    document_path: str,
    additional_instructions: str = "",
    save_dir: str = "",
) -> str:
    """Main function to proofread document and create track changes version on Mac."""

    if sys.platform not in SUPPORTED_OS:
        raise NotImplementedError(
            f"This application does not support running on '{sys.platform}'. "
            "Supported operating systems are: {', '.join(SUPPORTED_OS)}."
        )

    print(f"Processing document: {document_path}")

    # Use existing chunking function
    original_chunks = docx_to_chunks(document_path, 4000)
    print(f"Document split into {len(original_chunks)} chunks")

    # Process each chunk
    corrected_chunks = []
    for i, chunk in enumerate(original_chunks):
        print(f"Processing chunk {i+1}/{len(original_chunks)}")
        corrected_text = process_chunk_for_direct_edit(chunk, additional_instructions)
        corrected_chunks.append(corrected_text)

    # Create corrected document
    corrected_doc = create_corrected_document_from_chunks(
        document_path, original_chunks, corrected_chunks
    )

    # Set up save paths
    date = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
    name = Path(document_path).stem

    if save_dir:
        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
    else:
        save_path = Path(document_path).parent

    # Save corrected version first
    corrected_path = save_path / f"{name}_corrected_{date}.docx"
    corrected_doc.save(str(corrected_path))
    print(f"Corrected document saved: {corrected_path}")

    print("🔄 Attempting to create track changes document...")
    compare_documents_with_applescript(
        document_path,
        corrected_path,
    )

    return str(corrected_path)


# Integration with your existing code structure
def docx_to_chunks(file_path, chunk_size):
    """Your existing chunking function - keeping it unchanged."""
    doc = Document(file_path)

    chunks = []
    current_paragraph = ""
    current_chunk = ""

    for para in doc.paragraphs:
        current_paragraph = ""
        for run in para.runs:
            text = run.text
            if run.bold and run.italic:
                current_paragraph += "<b><i>" + text + "</i></b>"
            elif run.bold:
                current_paragraph += "<b>" + text + "</b>"
            elif run.italic:
                current_paragraph += "<i>" + text + "</i>"
            else:
                current_paragraph += text
        current_paragraph += (
            "  \n"  # Add a newline after each paragraph for readability
        )
        current_chunk += current_paragraph

        # Check if the current paragraph is too long and chunk it if necessary
        if len(current_chunk) > chunk_size:  # Adjust the chunk size as needed
            # If the paragraph is not too long, append it to the list
            chunks.append(current_chunk)
            current_chunk = ""

    # Add the remainder that is smaller than the chunk size.
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
