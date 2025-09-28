# Copyright caerulex 2024

"""Main entrypoint of doc-proofreader."""

from datetime import datetime
from docx import Document
from pathlib import Path
from dotenv import load_dotenv
import os
from doc_proofreader.prompts.system_prompts import DEFAULT_SYSTEM_PROMPT
from doc_proofreader.prompts.user_prompts import USER_PROMPT
from doc_proofreader.llm.client_factory import ClientFactory

load_dotenv()


def docx_to_formatted_text(file_path):
    doc = Document(file_path)
    formatted_text = ""

    for para in doc.paragraphs:
        for run in para.runs:
            text = run.text
            if run.bold and run.italic:
                formatted_text += "<b><i>" + text + "</i></b>"
            elif run.bold:
                formatted_text += "<b>" + text + "</b>"
            elif run.italic:
                formatted_text += "<i>" + text + "</i>"
            else:
                formatted_text += text
        formatted_text += "\n"  # Add a newline after each paragraph for readability

    return formatted_text


def chunk_text(text, chunk_size=2000):  # 12000
    # This function is aware of the HTML-like tags to avoid splitting them.
    # TODO(caerulex): Don't split up a sentence between two chunks.
    chunks = []
    current_chunk = ""
    words = text.split(" ")
    for word in words:
        if len(current_chunk) + len(word) < chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk)
            current_chunk = word + " "
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def docx_to_chunks(file_path, chunk_size):
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


def process_chunk_with_llm(
    chunk: str, additional_instructions: str, client, model: str = None
):
    print("Processing chunk...")
    messages = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
        {"role": "user", "content": chunk},
    ]
    if additional_instructions:
        messages.insert(2, {"role": "user", "content": additional_instructions})

    result = client.create_completion(
        messages=messages,
        model=model,
        temperature=0.2,
    )
    if result.strip() == "No errors were found.":
        result = ""
    print(result)
    return result


def aggregate_outputs(outputs: list[str]):
    # Simple aggregation - join all outputs.
    return " ".join(outputs)


def export_proofreads(document_path: str, output: str, save_dir: str):
    date = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
    name = Path(document_path).stem

    # Create the full path for the output file
    output_file_name = f"results_{name}_{date}.txt"
    if save_dir:
        save_path = Path(save_dir)
        if not save_path.exists() or not save_path.is_dir():
            # Create the directory if it does not exist
            save_path.mkdir(parents=True, exist_ok=True)
        output_file_path = save_path / output_file_name
    else:
        output_file_path = output_file_name

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(output)
    print(f"Results saved to '{output_file_path}'")


def proofread_document(
    document_path: str,
    additional_instructions: str = "",
    save_outputs: bool = True,
    save_dir: str = "",
    provider: str = None,
    model: str = None,
    estimate_cost: bool = False,
) -> str:
    # Create LLM client
    client = ClientFactory.create_client(provider=provider, model_name=model)

    # Get document content and estimate cost if requested
    if estimate_cost:
        doc_content = docx_to_formatted_text(document_path)
        cost = client.estimate_cost(doc_content)
        model_info = client.get_model_info()
        print(f"\n📊 Cost Estimation:")
        print(f"  Model: {model_info['name']} ({model_info['provider']})")
        print(f"  Estimated cost: ${cost:.4f}")
        print(f"  Context window: {model_info['context_window']:,} tokens")
        response = input("\nProceed with proofreading? (y/n): ")
        if response.lower() != 'y':
            print("Proofreading cancelled.")
            return ""

    chunks = docx_to_chunks(document_path, 27500)  # ~5000 words
    aggregated_output = aggregate_outputs(
        [
            process_chunk_with_llm(chunk, additional_instructions, client, model)
            for chunk in chunks
        ]
    )

    # Save the results to a text file
    if save_outputs:
        export_proofreads(document_path, aggregated_output, save_dir)

    return aggregated_output
