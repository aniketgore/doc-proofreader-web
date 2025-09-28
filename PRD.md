# Product Requirements Document: Multi-Model Support & UI Enhancement

## Executive Summary
Enhance the Doc-Proofreader tool to support multiple LLM providers through OpenRouter integration, enabling users to choose from various AI models for document proofreading. Subsequently, develop a web-based user interface to improve accessibility and user experience beyond command-line usage.

## Problem Statement
Current limitations:
- **Model Lock-in**: Tool only supports OpenAI's GPT-4o model, limiting flexibility and cost optimization
- **CLI-Only Access**: Command-line interface creates barrier for non-technical users
- **No Cost Visibility**: Users cannot estimate or track proofreading costs
- **Limited Model Choice**: Cannot leverage strengths of different models (Claude for nuanced editing, Gemini for speed, etc.)

## Goals & Success Metrics

### Goals
1. Enable multi-model support through OpenRouter integration
2. Maintain backward compatibility with existing OpenAI integration
3. Create intuitive web interface for document upload and proofreading
4. Provide cost transparency and model comparison capabilities

### Success Metrics
- Support for 5+ different LLM models
- Zero breaking changes for existing users
- 90% reduction in setup complexity for non-technical users
- <30 second time from file upload to proofreading start
- Cost estimation accuracy within 10% of actual charges

## User Stories

### Technical User
- As a developer, I want to choose different models based on document type and budget
- As a power user, I want to batch process multiple documents with different models
- As a cost-conscious user, I want to estimate costs before processing

### Non-Technical User
- As a writer, I want to upload my document through a web browser
- As an editor, I want to see proofreading progress in real-time
- As a user, I want to download corrected documents without using terminal

## Technical Requirements

### MVP (Phase 0) - OpenRouter Integration
**Timeline: 1 week**

#### Core Features
1. **Multi-Provider Support**
   - Abstract LLM client interface
   - OpenRouter client implementation
   - Provider selection via environment variables
   - Maintain existing OpenAI support

2. **Model Selection**
   - Support GPT-4o via OpenRouter
   - Support Claude-3.5-Sonnet
   - Support Gemini-1.5-Pro
   - Model selection via CLI argument

3. **Configuration Management**
   - Environment variable support for provider selection
   - API key management for multiple providers
   - Fallback to OpenAI if OpenRouter unavailable

#### Implementation
```python
# New file structure
doc_proofreader/
├── llm/
│   ├── __init__.py
│   ├── base_client.py      # Abstract base class
│   ├── openai_client.py    # OpenAI implementation
│   └── openrouter_client.py # OpenRouter implementation
```

#### CLI Interface
```bash
# Existing behavior (unchanged)
python -m doc_proofreader "document.docx"

# New model selection
python -m doc_proofreader "document.docx" --provider openrouter --model claude-3.5-sonnet

# Cost estimation
python -m doc_proofreader "document.docx" --estimate-cost
```

### Phase 1 - Enhanced Multi-Model Support
**Timeline: 2 weeks**

#### Features
1. **Advanced Model Management**
   - Model-specific prompt optimization
   - Dynamic chunk sizing based on model context window
   - Automatic model fallback on errors
   - Response format normalization across models

2. **Cost Management**
   - Pre-processing cost estimation
   - Real-time cost tracking
   - Cost comparison across models
   - Usage history logging

3. **Performance Optimization**
   - Parallel chunk processing
   - Intelligent caching for repeated documents
   - Model-specific rate limit handling
   - Retry logic with exponential backoff

4. **Enhanced CLI Features**
   - Model recommendation based on document type
   - Batch processing with progress bars
   - Output format selection (DOCX, PDF, TXT)
   - Diff view in terminal

#### Configuration File
```yaml
# config.yaml
providers:
  openrouter:
    api_key: ${OPENROUTER_API_KEY}
    base_url: https://openrouter.ai/api/v1

models:
  claude-3.5-sonnet:
    provider: openrouter
    context_window: 200000
    cost_per_1k_tokens: 0.003
    optimal_chunk_size: 8000
    temperature: 0.1

  gpt-4o:
    provider: [openai, openrouter]
    context_window: 128000
    cost_per_1k_tokens: 0.005
    optimal_chunk_size: 4000
    temperature: 0.2
```

### Phase 2 - Web UI Development
**Timeline: 3-4 weeks**

#### Architecture
- **Backend**: FastAPI server with WebSocket support
- **Frontend**: React/Next.js with Tailwind CSS
- **Storage**: Local SQLite for job tracking
- **Deployment**: Docker container with docker-compose

#### Core Features

1. **Document Management**
   - Drag-and-drop file upload
   - Multiple file format support (DOCX, TXT, RTF)
   - Document preview before processing
   - History of processed documents

2. **Proofreading Interface**
   - Model selection with descriptions
   - Cost estimation before processing
   - Real-time progress indicators
   - Live preview of corrections

3. **Results & Export**
   - Side-by-side comparison view
   - Accept/reject individual corrections
   - Export in multiple formats
   - Track changes visualization

4. **User Experience**
   - No authentication required (local use)
   - Responsive design for mobile/tablet
   - Keyboard shortcuts for power users
   - Dark mode support

#### UI Mockup Structure
```
┌─────────────────────────────────────────┐
│  Doc-Proofreader                    ⚙️ │
├─────────────────────────────────────────┤
│                                         │
│  📄 Drop your document here             │
│      or click to browse                 │
│                                         │
├─────────────────────────────────────────┤
│  Model Selection:                       │
│  ○ GPT-4o (Balanced)         $0.05/page│
│  ● Claude-3.5 (Nuanced)      $0.03/page│
│  ○ Gemini-1.5 (Fast)         $0.02/page│
│                                         │
│  ☑️ Show track changes                  │
│  ☑️ Custom instructions                 │
│                                         │
│  [Start Proofreading]                   │
└─────────────────────────────────────────┘
```

#### API Endpoints
```python
POST   /api/upload          # Upload document
POST   /api/proofread       # Start proofreading job
GET    /api/jobs/{id}       # Get job status
GET    /api/jobs/{id}/ws    # WebSocket for live updates
GET    /api/download/{id}   # Download corrected document
GET    /api/models          # List available models
POST   /api/estimate        # Estimate cost
```

#### Frontend Routes
```
/                   # Home/Upload page
/proofread/{jobId}  # Live proofreading view
/results/{jobId}    # Results and download
/history            # Previous documents
/settings           # API keys and preferences
```

## Non-Functional Requirements

### Performance
- Document processing should start within 5 seconds
- UI should load in <2 seconds
- Support documents up to 100,000 words
- Handle 10 concurrent proofreading jobs

### Security
- API keys stored encrypted
- No document data persisted without user consent
- HTTPS only for web interface
- Input sanitization for uploaded files

### Reliability
- Graceful degradation if models unavailable
- Automatic recovery from API failures
- Progress persistence across browser refresh
- Backup to local storage for critical data

### Usability
- Single-click processing for common use cases
- Mobile-responsive design
- Accessibility compliance (WCAG 2.1 AA)
- Intuitive error messages

## Dependencies & Risks

### Dependencies
- OpenRouter API availability
- Model API stability and pricing
- Python ecosystem for backend
- Modern browser support for frontend

### Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| OpenRouter API changes | High | Version lock API, implement adapter pattern |
| Model pricing increases | Medium | Cost alerts, model fallback options |
| Large document processing timeout | Medium | Implement chunking, background jobs |
| Browser compatibility issues | Low | Progressive enhancement, fallback UI |

## Timeline Summary

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| MVP | 1 week | OpenRouter integration, 3 models supported |
| Phase 1 | 2 weeks | Full multi-model support, cost management |
| Phase 2 | 3-4 weeks | Web UI, complete user experience |

Total: 6-7 weeks from start to full implementation

## Success Criteria
- [ ] Existing users experience no breaking changes
- [ ] Support for minimum 5 different LLM models
- [ ] Web UI accessible without technical knowledge
- [ ] Cost estimation accurate within 10%
- [ ] Processing time comparable to current CLI
- [ ] 90% user satisfaction in usability testing

## Future Enhancements (Post-Phase 2)
- Cloud deployment option
- User accounts and document history
- Collaborative proofreading
- Custom model fine-tuning
- API for third-party integrations
- Browser extension for online editing
- Mobile native applications