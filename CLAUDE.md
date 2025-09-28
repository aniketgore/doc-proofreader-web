# Doc-Proofreader Project Context

## Project Overview
A Python-based document proofreading tool that leverages OpenAI's GPT-4o model to proofread Microsoft Word documents (.docx). The tool can either output a list of corrections for review or make inline edits directly to the document.

## Tech Stack
- **Language**: Python 3.10+
- **Key Dependencies**:
  - `python-docx` - For Word document manipulation
  - `openai` - OpenAI API integration
  - `python-dotenv` - Environment variable management
- **Development Tools**:
  - `black` - Code formatting
  - `ruff` - Linting
  - `pytest` - Testing

## Project Structure
```
doc-proofreader/
├── doc_proofreader/          # Main package
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── cli.py                # CLI argument parsing
│   ├── proofread_document.py # Core proofreading logic
│   ├── proofread_document_inline.py # Inline editing logic
│   └── prompts/              # GPT prompts
│       ├── system_prompts.py
│       └── user_prompts.py
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_proofread_document.py
│   └── resources/            # Test documents
├── proofread_files/          # Output directory for processed docs
├── pyproject.toml            # Project configuration
├── README.md                 # User documentation
└── LICENSE                   # MIT License
```

## Key Features
1. **Standard Mode**: Outputs a list of suggested corrections for manual review
2. **Inline Mode** (`--inline`): Directly edits the document and creates a corrected version
   - On macOS: Automatically generates a track-changes document
3. **Custom Instructions**: Allows users to provide document-specific proofreading rules

## Development Commands

### Setup
```bash
# Create virtual environment
python -m venv .doc-proofreader_venv

# Activate virtual environment
source .doc-proofreader_venv/bin/activate  # macOS/Linux
# or
.doc-proofreader_venv\Scripts\activate  # Windows

# Install dependencies
pip install .

# Install dev dependencies
pip install -e ".[dev,test]"
```

### Code Quality
```bash
# Format code
black doc_proofreader/ tests/

# Run linter
ruff check doc_proofreader/ tests/

# Run tests
pytest tests/
```

### Running the Tool
```bash
# Standard mode
python -m doc_proofreader "path/to/document.docx"

# With custom instructions
python -m doc_proofreader "path/to/document.docx" --additional-instructions "your instructions"

# Inline editing mode
python -m doc_proofreader "path/to/document.docx" --inline
```

## Environment Variables
- `OPENAI_API_KEY`: Required. Store in `.env` file or set as environment variable

## Important Notes
- The `.env` file is gitignored and should never be committed
- Output files are saved to `proofread_files/` directory
- The inline mode is not yet compatible with custom instructions
- On macOS, track changes functionality requires Microsoft Word

## Current Branch
You're currently on the `edit-inline-feature` branch, which appears to be working on improvements to the inline editing functionality.

## Contact
Maintainer: caerulex (Discord)