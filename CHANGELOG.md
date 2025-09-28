# Changelog

All notable changes to Doc-Proofreader will be documented in this file.

## [0.4.0] - 2025-09-29

### 🚀 Major Features Added
- **Multi-Model Support**: Added support for 11+ LLM models via OpenRouter integration
- **Gemini 2.5 Pro Integration**: Default model with massive 1M token context window (2M chars!)
- **Provider Selection**: Choose between OpenAI (direct) and OpenRouter APIs
- **Cost Estimation**: Pre-processing cost calculation and confirmation
- **Smart Chunking**: Increased chunk size to 5,000 words (27,500 characters) for better efficiency

### 🎯 Models Supported
**Via OpenAI:**
- GPT-4o, GPT-4o-mini, GPT-4, GPT-3.5-turbo

**Via OpenRouter:**
- **Google Gemini**: gemini-2.5-pro (default), gemini-1.5-pro, gemini-1.5-flash
- **Anthropic Claude**: claude-3.5-sonnet, claude-3-opus, claude-3-haiku
- **OpenAI**: All models above
- **Open Source**: llama-3.1-70b, mixtral-8x7b

### ⚡ Performance Improvements
- **80% fewer API calls** for large documents (5K word chunks vs 750 word chunks)
- **Faster processing** with optimized chunking strategy
- **Lower costs** due to reduced API call overhead

### 🛠️ CLI Enhancements
- `--provider` flag: Choose between 'openai' and 'openrouter'
- `--model` flag: Select specific model
- `--estimate-cost` flag: Preview costs before processing
- Backward compatibility: Existing commands work unchanged

### 🔧 Technical Improvements
- **LLM Abstraction Layer**: Clean architecture for multiple providers
- **OpenRouter Headers**: Proper HTTP-Referer and X-Title headers
- **Environment Configuration**: Support for multiple API keys and providers
- **Error Handling**: Improved provider-specific error messages

### 📝 Configuration Files
- `.env.example`: Complete configuration template
- **Environment Variables**:
  - `LLM_PROVIDER`: openai/openrouter
  - `MODEL_NAME`: Default model selection
  - `OPENROUTER_API_KEY`: OpenRouter API key
  - `OPENAI_API_KEY`: OpenAI API key

### 📖 Documentation
- Updated README with multi-model examples
- Model comparison and cost information
- Setup instructions for both providers
- Usage examples for all supported models

### 🔄 Track Changes
- Maintained existing track changes functionality
- Works with all new models
- macOS AppleScript integration for automatic comparison

---

## [0.1.1] - Previous
- Initial release with OpenAI GPT-4o support
- Basic document proofreading
- Track changes support (macOS)
- CLI interface