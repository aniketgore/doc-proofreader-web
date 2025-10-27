# Doc-Proofreader

A powerful document proofreading tool that utilizes various LLM models including Google Gemini 2.5 Pro (2M context window!), OpenAI GPT, Anthropic Claude, and more via direct API or OpenRouter integration.

## Setting Up

### 1. Install Python.

Download and install Python from the official website. Ensure to check "Add Python to PATH" during installation.

The version of Python this repo was tested with was `3.11.6`, but an earlier version, like `3.10`, should probably work.

### 2. Set up the virtual environment.

Navigate to your project folder in the command line and run:

```bash
python -m venv .doc-proofreader_venv
```

The project folder is defined as `doc-proofreader` -- the top level folder of this git repository.

### 3. Activate the virtual environment.

If you use VSCode, it should automatically recognize the new environment. If you don't use VSCode, run:

- Windows: Run `.doc-proofreader_venv\Scripts\activate`.
- MacOS/Linux: Run `source .doc-proofreader_venv/bin/activate`.

### 4. Install the dependencies in the virtual environment.

Navigate to your project folder in the command line and run:

```bash
pip install .
```

### 5. Store your API tokens

Store your API tokens by putting them in a file OR adding them to your environment variables. You can use either OpenAI directly or OpenRouter for access to multiple models.

#### Method 1. Store in a File (recommended method)

This option is probably the simplest for beginners!

- Create a file called `.env` within the project folder
- Add your API keys to the file. Don't forget to save!

**For OpenAI (default):**
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

**For OpenRouter (access to multiple models):**
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_PROVIDER=openrouter
MODEL_NAME=gemini-2.5-pro  # default, or any supported model
```

See `.env.example` for all available configuration options.

#### Method 2. Add the key to the environment variables

There are two ways to do this. One is temporary, the other is permanent.

**A. Export on command line (temporary).**

You will need to re-run this command every time you open a new command line window.

```bash
export OPENAI_API_KEY="YourAPIKeyHere"
```

**B. Add to system or user environment variables (permanent). You only need to do this once.**

**Windows:** Press the Windows key. Search your applications for "Environment Variables". Add your API tokens as environment variables.

**MacOS:** Edit the `~/.zshrc` file. Add the line:

```bash
export OPENAI_API_KEY="YourAPIKeyHere"
```

Then run:

```bash
source ~/.zshrc
```

**Linux:** Edit the `~/.bashrc` file. Add the same line as for MacOS, above. Then run:

```bash
source ~/.bashrc
```

### 6. Install Streamlit (for GUI - optional)

If you want to use the graphical interface:

```bash
pip install streamlit
```

## Quick Start (GUI)

### Easy Launcher (macOS/Linux)

The easiest way to run the GUI is using the launcher script:

```bash
./launch_proofreader.sh
```

**Features:**
- 🚀 Automatically activates virtual environment
- 🌐 Opens your browser to the app
- 🛑 Handles cleanup when you press Ctrl+C
- ✨ No manual commands needed!

**First time setup:**
1. Make sure the script is executable: `chmod +x launch_proofreader.sh`
2. Run it: `./launch_proofreader.sh`
3. The app will open in your browser at http://localhost:8501

**Alternative manual launch:**
```bash
streamlit run streamlit_app.py
```

### Streamlit GUI Features

The web interface provides:
- 📤 Easy file upload via drag-and-drop
- 🎛️ Visual model and provider selection
- 📋 Two modes: List corrections or inline editing
- 📝 Custom instructions input
- 💾 One-click download of results
- 📊 Progress tracking and status updates

## Usage

### Basic Usage

**Default with OpenAI (GPT-4o):**
```bash
python -m doc_proofreader "path to your docx file"
```

**Default with OpenRouter (Gemini 2.5 Pro - Recommended!):**
```bash
python -m doc_proofreader "path to your docx file" --provider openrouter
```

### Using Different Models

**Claude 3.5 Sonnet via OpenRouter:**
```bash
python -m doc_proofreader "path to your docx file" --provider openrouter --model claude-3.5-sonnet
```

**Gemini 2.5 Pro (2M context - handles entire books!):**
```bash
python -m doc_proofreader "path to your docx file" --provider openrouter --model gemini-2.5-pro
# Note: This is the default when using --provider openrouter
```

**GPT-4o Mini (cheaper option):**
```bash
python -m doc_proofreader "path to your docx file" --model gpt-4o-mini
```

### Cost Estimation

Estimate the cost before processing:
```bash
python -m doc_proofreader "path to your docx file" --estimate-cost
```

### Advanced Chunking Options

**Auto-optimize chunks for your model:**
```bash
python -m doc_proofreader "document.docx" --chunk auto
# Automatically sets optimal chunk size based on model's context window
```

**Custom chunk sizes:**
```bash
# Process in 10,000 word chunks (great for large documents)
python -m doc_proofreader "document.docx" --chunk 10000w

# Process in 50,000 character chunks
python -m doc_proofreader "document.docx" --chunk 50000c

# Small chunks for precise control
python -m doc_proofreader "document.docx" --chunk 2000w
```

### Performance Features

**Parallel Processing** (automatic for multiple chunks):
- Processes multiple chunks simultaneously
- 3x faster for large documents
- Maintains order and quality

**Example with Gemini 2.5 Pro + Auto Chunking:**
```bash
# Best performance: entire 50K word document in 1 chunk!
python -m doc_proofreader "large_document.docx" --provider openrouter --chunk auto
```

### Custom Instructions

You can pass additional information/instructions to the model, custom to your document, following this example:

```bash
python -m doc_proofreader "path to your docx file" --additional-instructions "your custom instructions"
```

Custom instructions might look like, `"half elf" should not be corrected to "half-elf".`

You should be able to run this example as-is:

```bash
python -m doc_proofreader "./tests/resources/test_doc.docx" --additional-instructions '"half elf" should not be corrected to "half-elf".'
```

There is also an inline option where the app will directly proofread your input file.

```bash
python -m doc_proofreader "path to your docx file" --inline
```

This option will output a document with all changes. On Mac, it will also automatically attempt to create a track changes document to see clearly all modifications for easy review.

The inline option is currently not compatible with custom instructions.

## Chunking Strategy Guide

### Recommended Chunk Sizes by Use Case:

| Use Case | Chunk Size | Example | Best For |
|----------|------------|---------|----------|
| **Speed** | `--chunk auto` | Entire doc in 1-2 chunks | Large docs, Gemini 2.5 Pro |
| **Balance** | `--chunk 10000w` | 10K words | Most documents |
| **Precision** | `--chunk 3000w` | 3K words | Complex docs, careful review |
| **Conservative** | `--chunk 15000c` | 15K characters | Older models, safety |

### Model-Specific Recommendations:

| Model | Optimal Chunk | Max Document Size |
|-------|---------------|-------------------|
| **Gemini 2.5 Pro** | `auto` (200K chars) | Entire novels |
| **Claude 3.5 Sonnet** | `auto` (100K chars) | Long articles |
| **GPT-4o** | `auto` (80K chars) | Standard docs |
| **GPT-3.5** | `5000w` | Smaller docs |

## Available Models

### Via OpenAI (default provider):
- `gpt-4o` - Most capable, balanced cost (default)
- `gpt-4o-mini` - Faster, cheaper alternative
- `gpt-4` - Previous generation
- `gpt-3.5-turbo` - Fastest, most economical

### Via OpenRouter:
- **OpenAI Models:** All OpenAI models listed above
- **Google Gemini:**
  - `gemini-2.5-pro` - **RECOMMENDED: Massive 2M token context window!** (default for OpenRouter)
  - `gemini-1.5-pro` - Large context window (1M tokens)
  - `gemini-1.5-flash` - Faster Gemini option
- **Anthropic Claude:**
  - `claude-3.5-sonnet` - Best for nuanced editing
  - `claude-3-opus` - Most capable Claude model
  - `claude-3-haiku` - Fast and economical
- **Open Models:**
  - `llama-3.1-70b` - Open source alternative
  - `mixtral-8x7b` - Efficient mixture of experts model

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError for `openai`

**Symptom:** Error indicating the `openai` module is not found.  This dependency should be included if all setup steps are followed.

**Solution:** Install the `openai` package within your virtual environment using `pip install openai`.

### Issue 2: Providing the OpenAI API Key

**Symptom:** Uncertainty about where to add the OpenAI API key.

**Solution:** 
- Create a `.env` file in your project directory.
- Add `OPENAI_API_KEY=your_api_key_here` to the file.
- Ensure `python-dotenv` is installed using `pip install python-dotenv`. This dependency should be included if all setup steps are followed.

## Contact

If you need help or want to report a bug, please DM caerulex on discord.
