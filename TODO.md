# Vuhitra CLI - TODO / Terms of Reference (ToR)

## Project Overview

Vuhitra CLI is a Docker-based AI-powered command-line interface for data analytics and development workflows. It leverages local OLLAMA models for AI capabilities while providing a robust infrastructure for prompt caching, heuristics, and data processing.

## Project Philosophy

### Key Principles
1. **Docker-First Architecture**: All components run in containers; no host-based installation required
2. **Local AI Models**: Exclusive use of OLLAMA models for privacy and performance
3. **Intelligent Caching**: Smart prompt management using heuristics and similarity matching
4. **Data Analytics Focus**: First-class support for R, Python, and PySpark workflows
5. **Development-Oriented**: Special dev mode for iterative application development

## Technical Architecture

### Core Components

#### 1. CLI Service
- **Purpose**: Main Python-based command-line interface
- **Pre-installed Libraries**:
  - NLP: spaCy, VADER (sentiment analysis)
  - Data Analytics: pandas, numpy, scikit-learn
  - AI Integration: OLLAMA client libraries
- **Capabilities**:
  - Interact with OLLAMA models
  - Manage prompt caching and heuristics
  - Orchestrate data processing workflows
  - Support MCP (stdio ONLY) integration
  - RAG (Retrieval-Augmented Generation) support

#### 2. Redis (OSS >= 7.2)
- **Purpose**: Vector store for RAG and temporary data storage
- **Use Cases**:
  - Store and retrieve temporary DataFrames
  - Vector storage for RAG implementations
  - Session data and intermediate results
  - Data analytics cache for R, Python, PySpark

#### 3. Elasticsearch
- **Purpose**: Heuristic and prompt similarity caching
- **Features**:
  - **Heuristics Storage**: Behavior patterns of prompts (always enabled)
  - **Prompt Cache**: Similarity-based prompt caching (disabled by default)
  - **Signature Generation**: NLP-based or hash-based prompt signatures
- **Configuration**:
  - Heuristics: ENABLED by default
  - Prompt cache: DISABLED by default

#### 4. Apache Spark
- **Image**: `ghcr.io/nexus-mdg/spark-3.5:latest`
- **Purpose**: Distributed data processing
- **Integration**: PySpark workflows from CLI

#### 5. Sandbox Service
- **Purpose**: Isolated workspace for file processing
- **Characteristics**:
  - Shared volume with CLI service
  - No fixed persistent volumes
  - Temporary file hosting
  - Files uploaded → processed → deleted workflow

### AI Model Strategy

#### Primary Models
1. **Llama 8B**: General knowledge and reasoning tasks
2. **Qwen Coder 7B**: Code generation and development tasks

#### Model Selection
- Default to lightweight models (8B, 7B parameters)
- Support larger models when GPU resources permit
- Model selection via configuration parameter

#### OLLAMA Integration
- Configurable OLLAMA server IP (can be external or containerized)
- API-based communication
- Model download and management via OLLAMA

## Development Features

### Dev Mode
A specialized mode for iterative application development:

#### Characteristics
- **Language-Specific Isolation**: Clear separation for future extensibility
  - Python (initial support)
  - JavaScript (future)
  - Java (future)
  - Other languages (extensible architecture)
- **Iteration Support**: Configurable max iterations
- **Hot Reload**: File watching and auto-reload capabilities
- **Debug Integration**: Enhanced logging and debugging tools

#### Non-Dev Mode
- Production-like execution
- Limited iterations
- Optimized for single-run workflows

## Docker Infrastructure

### Docker Compose Configuration

```yaml
services:
  - cli
  - redis
  - elasticsearch
  - spark
  - sandbox
```

### Build Optimization
- **BuildKit**: Modern Docker build engine
- **Layer Caching**: 
  - APK packages (Alpine Linux packages)
  - pip packages (Python dependencies)
  - Local mount caching to avoid re-downloads
- **Multi-stage Builds**: Minimal final image size

## Configuration Parameters

### Environment Variables

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `MAX_CONTEXT_FILE_SIZE` | Maximum file size for context inclusion | 10MB | `10485760` |
| `MAX_UPLOADED_FILE_SIZE` | Maximum upload size in sandbox | 100MB | `104857600` |
| `MODEL` | OLLAMA model to use | `llama3:8b` | `qwen2.5-coder:7b` |
| `OLLAMA_IP` | OLLAMA server address | `http://ollama:11434` | `http://192.168.1.100:11434` |
| `MAX_ITERATIONS_DEV` | Max iterations in dev mode | 50 | `100` |
| `MAX_ITERATIONS_PROD` | Max iterations in non-dev mode | 5 | `10` |
| `ENABLE_PROMPT_CACHE` | Enable prompt similarity caching | `false` | `true` |
| `ENABLE_HEURISTICS` | Enable heuristic storage | `true` | `true` |

### Special Keywords in Prompts
To be defined during implementation iterations. Examples:
- `@devmode`: Switch to development mode
- `@upload`: Upload file to sandbox
- `@analyze`: Trigger data analytics workflow
- `@spark`: Execute PySpark job
- `@cache`: Force cache this prompt
- `@nocache`: Skip cache for this prompt

## Extension Points

### MCP (Model Context Protocol)
- **Supported Mode**: stdio ONLY
- **Purpose**: Extend CLI capabilities with external tools
- **Integration**: Python-based MCP client

### RAG (Retrieval-Augmented Generation)
- **Vector Store**: Redis with vector capabilities
- **Use Cases**:
  - Document Q&A
  - Code repository search
  - Knowledge base integration
- **Embeddings**: Generated via OLLAMA models

## Workflow Examples

### 1. Data Analytics Workflow
```
User uploads CSV → Sandbox receives file → CLI processes with pandas → 
Results stored in Redis → Spark job for heavy processing → 
Results returned → Temporary files deleted
```

### 2. Code Generation (Dev Mode)
```
User prompt → Check Elasticsearch cache → 
If miss: Query OLLAMA (Qwen Coder) → Store heuristics → 
Generate code → Iterate based on feedback → 
Store final result in cache
```

### 3. Document Q&A with RAG
```
Documents ingested → Embeddings generated via OLLAMA → 
Stored in Redis vector store → User query → 
Retrieve relevant chunks → Augment prompt → 
Query OLLAMA with context → Return answer
```

## Implementation Success Criteria

### Documentation Deliverables
1. ✅ **TODO.md** (this file): Complete project description and architecture
2. ✅ **IMPLEMENTATION.md**: Step-by-step implementation guide
3. ✅ **prompts/*.md**: Individual prompt files for each implementation step

### Functional Requirements
- [ ] Docker Compose setup with all services
- [ ] CLI service with Python and required libraries
- [ ] Redis integration for vector storage and caching
- [ ] Elasticsearch integration for heuristics and prompt cache
- [ ] Apache Spark integration
- [ ] Sandbox service with shared volumes
- [ ] OLLAMA model integration
- [ ] Configuration parameter handling
- [ ] Dev mode implementation
- [ ] MCP support (stdio)
- [ ] RAG support
- [ ] BuildKit optimization with caching

### Quality Requirements
- [ ] All services start successfully via docker-compose
- [ ] CLI can communicate with all services
- [ ] Models can be loaded and queried
- [ ] Cache and heuristics work correctly
- [ ] Files can be uploaded, processed, and cleaned up
- [ ] Dev mode provides iterative development experience
- [ ] Documentation is complete and accurate

## Development Roadmap

### Phase 1: Foundation (Weeks 1-2)
- Docker Compose setup
- Basic CLI structure
- Service connectivity
- OLLAMA integration

### Phase 2: Core Features (Weeks 3-4)
- Elasticsearch heuristics
- Redis vector store
- Prompt caching
- File handling in sandbox

### Phase 3: Analytics (Weeks 5-6)
- Pandas/NumPy integration
- PySpark workflows
- Data pipeline examples
- Temporary data management

### Phase 4: Advanced Features (Weeks 7-8)
- Dev mode implementation
- MCP integration
- RAG implementation
- NLP enhancements (spaCy, VADER)

### Phase 5: Optimization (Weeks 9-10)
- BuildKit caching optimization
- Performance tuning
- Documentation completion
- Testing and validation

## Security Considerations

### Data Privacy
- All AI processing happens locally (OLLAMA)
- No external API calls for model inference
- Data stays within Docker network

### File Handling
- Sandbox isolation for uploaded files
- Automatic cleanup of temporary files
- Size limits to prevent DoS

### Network Security
- Services communicate via Docker network
- Configurable external OLLAMA connection
- No exposed ports except necessary endpoints

## Performance Considerations

### Resource Management
- GPU acceleration for OLLAMA (when available)
- Spark resource allocation
- Redis memory limits
- Elasticsearch heap size

### Caching Strategy
- Prompt signature generation (NLP vs hash trade-off)
- Cache invalidation rules
- Heuristics learning over time

## Future Enhancements

### Planned Features
- [ ] Additional language support in dev mode (JS, Java, Go, Rust)
- [ ] Web UI for non-CLI users
- [ ] Workflow automation and scheduling
- [ ] Multi-model ensemble support
- [ ] Advanced RAG techniques (HyDE, ReRank)
- [ ] Distributed caching across multiple nodes
- [ ] Plugin architecture for custom processors

### Community Features
- [ ] Public model registry
- [ ] Shared heuristics database
- [ ] Community prompt templates
- [ ] Example workflows repository

## Contributing

### Development Setup
1. Clone repository
2. Ensure Docker and Docker Compose installed
3. Run `docker-compose up -d`
4. Access CLI via `docker exec -it vuhitra-cli /bin/bash`

### Code Standards
- Python: PEP 8
- Docker: Best practices (multi-stage, minimal layers)
- Documentation: Markdown with clear examples

## License

MIT License - See LICENSE file for details

## Contact & Support

- **Repository**: https://github.com/Nexus-mdg/vuhitra-cli
- **Issues**: GitHub Issues
- **Documentation**: See /docs directory

---

**Last Updated**: 2025-11-06
**Version**: 0.1.0 (Initial ToR)
