# Vuhitra CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)

**Vuhitra CLI** - A Docker-based AI-powered command-line interface for intelligent data analytics and development workflows using local OLLAMA models.

## 🚀 Overview

Vuhitra CLI is a comprehensive, Docker-first CLI tool that leverages local AI models (via OLLAMA) to provide intelligent data processing, code generation, and development capabilities. It combines the power of AI with robust data analytics infrastructure, all running locally without external API dependencies.

### Key Features

- 🤖 **Local AI Models**: Exclusive use of OLLAMA models (Llama 8B, Qwen Coder 7B, and more)
- 🐳 **Docker-First**: Fully containerized architecture - no host installation needed
- 🧠 **Intelligent Caching**: Smart prompt management with heuristics and similarity matching
- 📊 **Data Analytics**: First-class support for Python, R, and PySpark workflows
- 🔧 **Dev Mode**: Iterative development environment for rapid application building
- 🎯 **RAG Support**: Retrieval-Augmented Generation with vector storage
- 🔌 **MCP Integration**: Model Context Protocol support for extensibility
- ⚡ **Performance Optimized**: BuildKit caching, multi-stage builds, efficient resource usage

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🏗️ Architecture

Vuhitra CLI consists of 5 Docker services orchestrated via Docker Compose:

```
┌─────────────────────────────────────────────────────────────┐
│                         Vuhitra CLI                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │   CLI   │◄─┤ Elasticsearch │  │   Apache Spark      │  │
│  │ Service │  │  (Heuristics  │  │  (Data Processing)  │  │
│  │         │  │   & Cache)    │  │                     │  │
│  └────┬────┘  └──────────────┘  └─────────────────────┘  │
│       │                                                    │
│       ├──────►┌──────────────┐  ┌─────────────────────┐  │
│       │       │    Redis     │  │      Sandbox        │  │
│       │       │ (Vector Store│  │  (File Processing)  │  │
│       └──────►│ & Data Cache)│  │                     │  │
│               └──────────────┘  └─────────────────────┘  │
│                                                           │
│                          ▼                                │
│                   OLLAMA Server                           │
│              (Local AI Model Host)                        │
└───────────────────────────────────────────────────────────┘
```

### Services

1. **CLI Service**: Python-based CLI with NLP (spaCy, VADER) and data analytics (pandas, numpy, scikit-learn)
2. **Redis (>= 7.2)**: Vector storage for RAG and temporary DataFrame caching
3. **Elasticsearch**: Heuristics storage and prompt similarity caching
4. **Apache Spark**: Distributed data processing via PySpark
5. **Sandbox**: Isolated workspace for temporary file operations

## 📦 Prerequisites

- **Docker Engine** >= 24.0
- **Docker Compose** >= 2.20
- **OLLAMA** (can run on same host or remote server)
- **8GB+ RAM** (16GB+ recommended)
- **GPU** with CUDA support (optional, for larger models)

### Install Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify installation
docker --version
docker-compose --version
```

### Install OLLAMA

```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended models
ollama pull llama3:8b
ollama pull qwen2.5-coder:7b
```

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nexus-mdg/vuhitra-cli.git
   cd vuhitra-cli
   ```

2. **Configure environment**:
   ```bash
   cp config/.env.template .env
   # Edit .env to set OLLAMA_IP and other parameters
   ```

3. **Start services**:
   ```bash
   docker-compose up -d
   ```

4. **Verify services are healthy**:
   ```bash
   docker-compose ps
   ```

5. **Run your first command**:
   ```bash
   docker-compose exec cli vuhitra --help
   docker-compose exec cli vuhitra chat "What is Python?"
   ```

## 📚 Documentation

This repository includes comprehensive documentation:

- **[TODO.md](TODO.md)**: Complete Terms of Reference and project description
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)**: Step-by-step implementation guide with 20 detailed steps
- **[prompts/](prompts/)**: Individual prompt files for each implementation step

### Quick Links

- [Architecture Overview](TODO.md#technical-architecture)
- [Implementation Guide](IMPLEMENTATION.md)
- [Configuration Parameters](TODO.md#configuration-parameters)
- [Implementation Prompts](prompts/README.md)

## 📁 Project Structure

```
vuhitra-cli/
├── cli/                      # CLI application
│   ├── src/                 # Source code
│   │   └── cli/            # Main package
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # CLI container
├── docker/                  # Docker configurations
│   ├── sandbox/            # Sandbox service
│   └── configs/            # Service configs
├── config/                  # Configuration files
│   └── .env.template       # Environment template
├── docs/                    # Documentation
├── tests/                   # Test suite
├── examples/                # Example workflows
├── prompts/                 # Implementation prompts
├── docker-compose.yml       # Service orchestration
├── TODO.md                  # Project ToR
├── IMPLEMENTATION.md        # Implementation guide
└── README.md               # This file
```

## ⚙️ Configuration

### Environment Variables

Create `.env` from template and configure:

```env
# OLLAMA Configuration
OLLAMA_IP=http://host.docker.internal:11434
MODEL=llama3:8b

# File Size Limits (bytes)
MAX_CONTEXT_FILE_SIZE=10485760        # 10MB
MAX_UPLOADED_FILE_SIZE=104857600      # 100MB

# Iteration Limits
MAX_ITERATIONS_DEV=50
MAX_ITERATIONS_PROD=5

# Feature Flags
ENABLE_PROMPT_CACHE=false
ENABLE_HEURISTICS=true

# Service URLs (internal)
REDIS_URL=redis://redis:6379
ELASTICSEARCH_URL=http://elasticsearch:9200
SPARK_MASTER=spark://spark:7077

# Logging
LOG_LEVEL=INFO
```

See [TODO.md](TODO.md#configuration-parameters) for complete parameter reference.

## 💡 Usage Examples

### Chat with AI

```bash
# Basic chat
vuhitra chat "Explain machine learning"

# Streaming response
vuhitra chat --stream "Write a Python function to sort a list"

# Use specific model
vuhitra chat --model qwen2.5-coder:7b "Generate a REST API"
```

### Data Analysis

```bash
# Analyze CSV file
vuhitra analyze data.csv

# Cache analysis results
vuhitra analyze data.csv --cache-key my-analysis

# PySpark job
vuhitra spark submit analysis.py
```

### Development Mode

```bash
# Start Python dev mode
vuhitra dev --language python

# Custom iteration limit
vuhitra dev --language python --max-iterations 100
```

### Model Management

```bash
# List available models
vuhitra models list

# Pull new model
vuhitra models pull llama3.1:8b
```

### Cache Management

```bash
# Check cache status
vuhitra cache status

# Clear cache
vuhitra cache clear
```

## 🛠️ Development

### Building from Source

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build services
docker-compose build

# Rebuild specific service
docker-compose build cli
```

### Running Tests

```bash
# Run all tests
docker-compose run --rm cli pytest

# With coverage
docker-compose run --rm cli pytest --cov=cli

# Specific test
docker-compose run --rm cli pytest tests/unit/test_config.py
```

### Development Workflow

1. Make code changes in `cli/src/`
2. Rebuild CLI service: `docker-compose build cli`
3. Restart service: `docker-compose restart cli`
4. Run tests: `docker-compose run --rm cli pytest`

### Implementation Steps

Follow the [IMPLEMENTATION.md](IMPLEMENTATION.md) guide for complete development process:

1. Project Structure Setup
2. Docker Compose Foundation
3. CLI Dockerfile with BuildKit
4. CLI Core Application
5. OLLAMA Integration
6. Elasticsearch Integration
7. Redis Integration
8. Sandbox Service
9. Data Analytics
10. Spark Integration
11. Dev Mode
12. MCP Support
13. RAG Implementation
14. NLP Enhancements
15. Configuration Management
16. BuildKit Optimization
17. Testing Infrastructure
18. Documentation
19. Security Hardening
20. Final Integration

Each step has a detailed prompt file in `prompts/`.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`docker-compose run --rm cli pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards

- **Python**: PEP 8 compliance
- **Docker**: Multi-stage builds, minimal layers
- **Documentation**: Clear markdown with examples
- **Tests**: Pytest with >80% coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OLLAMA](https://ollama.ai/) for local AI model hosting
- [spaCy](https://spacy.io/) for NLP capabilities
- [Apache Spark](https://spark.apache.org/) for distributed processing
- [Elasticsearch](https://www.elastic.co/) for search and analytics
- [Redis](https://redis.io/) for caching and vector storage

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Nexus-mdg/vuhitra-cli/issues)
- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory

## 🗺️ Roadmap

See [TODO.md](TODO.md#development-roadmap) for detailed roadmap.

### Current Version: 0.1.0 (In Development)

**Phase 1**: Foundation (Weeks 1-2)
- ✅ Project structure and documentation
- ⏳ Docker Compose setup
- ⏳ CLI core implementation
- ⏳ OLLAMA integration

**Phase 2**: Data Layer (Weeks 3-4)
- ⏳ Elasticsearch integration
- ⏳ Redis vector store
- ⏳ Spark integration

**Phase 3**: Advanced Features (Weeks 5-6)
- ⏳ Dev mode
- ⏳ MCP support
- ⏳ RAG implementation

**Phase 4**: Polish (Weeks 7-8)
- ⏳ Testing and optimization
- ⏳ Documentation completion
- ⏳ Security hardening

### Future Enhancements

- Additional language support (JavaScript, Java, Go, Rust)
- Web UI interface
- Multi-model ensemble
- Advanced RAG techniques
- Plugin architecture

---

**Made with ❤️ by Nexus-mdg**

**Version**: 0.1.0 (Initial Development)  
**Last Updated**: 2025-11-06
