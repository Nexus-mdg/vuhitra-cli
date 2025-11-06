# Vuhitra CLI - Implementation Guide

This document provides a step-by-step guide to implement the Vuhitra CLI project. Each step has a corresponding prompt file in the `prompts/` directory.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Implementation Steps](#implementation-steps)
3. [Testing Strategy](#testing-strategy)
4. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- Docker Engine >= 24.0
- Docker Compose >= 2.20
- Git
- Text editor or IDE
- 8GB+ RAM (16GB+ recommended)
- GPU with CUDA support (optional, for larger models)

### Required Knowledge
- Docker and containerization
- Python programming
- Basic understanding of:
  - Redis
  - Elasticsearch
  - Apache Spark
  - AI/ML concepts

## Implementation Steps

### Step 1: Project Structure Setup
**Goal**: Create the foundational directory structure and configuration files.

**Prompt File**: `prompts/01-project-structure.md`

**Tasks**:
- Create directory structure
- Initialize Git repository (if needed)
- Create `.gitignore`
- Setup basic README.md
- Create placeholder directories for:
  - `cli/` - CLI application code
  - `docker/` - Dockerfiles and build scripts
  - `config/` - Configuration files
  - `docs/` - Documentation
  - `tests/` - Test files
  - `examples/` - Example workflows

**Deliverables**:
```
vuhitra-cli/
├── cli/
│   ├── src/
│   ├── requirements.txt
│   └── Dockerfile
├── docker/
│   ├── sandbox/
│   └── configs/
├── config/
│   └── .env.template
├── docs/
├── tests/
├── examples/
├── prompts/
├── docker-compose.yml
├── .gitignore
├── README.md
├── TODO.md
└── IMPLEMENTATION.md
```

**Validation**:
- All directories exist
- .gitignore properly excludes build artifacts
- README provides basic project overview

---

### Step 2: Docker Compose Foundation
**Goal**: Create the base docker-compose.yml with all required services.

**Prompt File**: `prompts/02-docker-compose.md`

**Tasks**:
- Define all 5 services (cli, redis, elasticsearch, spark, sandbox)
- Configure networks
- Setup volume mounts
- Define environment variables
- Configure service dependencies
- Setup healthchecks

**Key Configurations**:

**Redis**:
```yaml
redis:
  image: redis:7.2-alpine
  volumes:
    - redis-data:/data
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
```

**Elasticsearch**:
```yaml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
  environment:
    - discovery.type=single-node
    - xpack.security.enabled=false
  healthcheck:
    test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
```

**Spark**:
```yaml
spark:
  image: ghcr.io/nexus-mdg/spark-3.5:latest
  environment:
    - SPARK_MODE=master
```

**Sandbox**:
```yaml
sandbox:
  build:
    context: ./docker/sandbox
  volumes:
    - sandbox-workspace:/workspace
```

**CLI**:
```yaml
cli:
  build:
    context: ./cli
    dockerfile: Dockerfile
  volumes:
    - sandbox-workspace:/workspace
    - ./cli/src:/app/src
  environment:
    - OLLAMA_IP=${OLLAMA_IP}
    - MODEL=${MODEL}
  depends_on:
    - redis
    - elasticsearch
    - spark
```

**Deliverables**:
- `docker-compose.yml`
- `.env.template`
- Network and volume definitions

**Validation**:
```bash
docker-compose config  # Validate syntax
docker-compose up -d   # Services start without errors
docker-compose ps      # All services healthy
```

---

### Step 3: CLI Dockerfile with BuildKit Optimization
**Goal**: Create optimized Dockerfile for CLI service with caching.

**Prompt File**: `prompts/03-cli-dockerfile.md`

**Tasks**:
- Create multi-stage Dockerfile
- Configure BuildKit caching for APK and pip
- Install Python dependencies
- Install NLP libraries (spaCy, VADER)
- Install data analytics libraries (pandas, numpy, scikit-learn)
- Setup OLLAMA client
- Configure entrypoint

**Dockerfile Structure**:
```dockerfile
# syntax=docker/dockerfile:1.4

# Stage 1: Base with system dependencies
FROM python:3.11-alpine AS base

# Enable BuildKit cache mounts
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers

# Stage 2: Dependencies
FROM base AS dependencies

WORKDIR /app

# Cache pip packages
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_sm

# Stage 3: Final
FROM python:3.11-alpine

# Copy installed packages from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=dependencies /app /app

WORKDIR /app
COPY src/ ./src/

ENTRYPOINT ["python", "-m", "cli.main"]
```

**requirements.txt**:
```
# AI/ML
ollama>=0.1.0

# NLP
spacy>=3.7.0
vaderSentiment>=3.3.2

# Data Analytics
pandas>=2.1.0
numpy>=1.24.0
scikit-learn>=1.3.0

# Database Clients
redis>=5.0.0
elasticsearch>=8.11.0

# Spark
pyspark>=3.5.0

# Utilities
python-dotenv>=1.0.0
click>=8.1.0
pydantic>=2.0.0
```

**Deliverables**:
- `cli/Dockerfile`
- `cli/requirements.txt`
- `cli/.dockerignore`

**Validation**:
```bash
DOCKER_BUILDKIT=1 docker build --progress=plain -t vuhitra-cli:test ./cli
docker run --rm vuhitra-cli:test --version
```

---

### Step 4: CLI Core Application Structure
**Goal**: Implement the basic CLI application framework.

**Prompt File**: `prompts/04-cli-core.md`

**Tasks**:
- Create main CLI entry point
- Implement configuration management
- Setup logging
- Create service clients (Redis, Elasticsearch, OLLAMA)
- Implement command routing
- Add version and help commands

**Directory Structure**:
```
cli/src/
├── cli/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration management
│   ├── logger.py            # Logging setup
│   ├── commands/            # CLI commands
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── analyze.py
│   │   └── dev.py
│   ├── services/            # External service clients
│   │   ├── __init__.py
│   │   ├── ollama_client.py
│   │   ├── redis_client.py
│   │   ├── elastic_client.py
│   │   └── spark_client.py
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── prompt_signature.py
│       └── file_handler.py
```

**Key Files**:

**main.py**:
```python
import click
from cli.config import Config
from cli.logger import setup_logger

@click.group()
@click.version_option(version='0.1.0')
@click.pass_context
def cli(ctx):
    """Vuhitra CLI - AI-powered data analytics and development."""
    ctx.obj = Config()
    setup_logger(ctx.obj.log_level)

@cli.command()
@click.argument('prompt')
@click.pass_context
def chat(ctx, prompt):
    """Send a prompt to the AI model."""
    # Implementation in prompts/04-cli-core.md
    pass

if __name__ == '__main__':
    cli()
```

**config.py**:
```python
from pydantic import BaseSettings

class Config(BaseSettings):
    # OLLAMA
    ollama_ip: str = "http://ollama:11434"
    model: str = "llama3:8b"
    
    # File sizes
    max_context_file_size: int = 10 * 1024 * 1024  # 10MB
    max_uploaded_file_size: int = 100 * 1024 * 1024  # 100MB
    
    # Iterations
    max_iterations_dev: int = 50
    max_iterations_prod: int = 5
    
    # Features
    enable_prompt_cache: bool = False
    enable_heuristics: bool = True
    
    # Service endpoints
    redis_url: str = "redis://redis:6379"
    elasticsearch_url: str = "http://elasticsearch:9200"
    spark_master: str = "spark://spark:7077"
    
    class Config:
        env_file = ".env"
```

**Deliverables**:
- CLI application structure
- Configuration management
- Basic commands (version, help, chat)
- Service client stubs

**Validation**:
```bash
docker-compose run --rm cli --help
docker-compose run --rm cli --version
docker-compose run --rm cli chat "Hello, world!"
```

---

### Step 5: OLLAMA Integration
**Goal**: Implement OLLAMA model integration for AI inference.

**Prompt File**: `prompts/05-ollama-integration.md`

**Tasks**:
- Create OLLAMA client wrapper
- Implement model loading
- Implement prompt submission
- Handle streaming responses
- Error handling and retries
- Model validation

**Key Implementation**:
```python
# cli/src/cli/services/ollama_client.py
import requests
from typing import Generator, Optional

class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        
    def generate(self, prompt: str, stream: bool = False) -> str | Generator:
        """Generate response from OLLAMA."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        
        response = requests.post(url, json=payload, stream=stream)
        response.raise_for_status()
        
        if stream:
            return self._stream_response(response)
        else:
            return response.json()['response']
    
    def list_models(self) -> list:
        """List available models."""
        response = requests.get(f"{self.base_url}/api/tags")
        return response.json()['models']
```

**Deliverables**:
- OLLAMA client implementation
- Model management commands
- Streaming support
- Error handling

**Validation**:
```bash
# Requires OLLAMA running
docker-compose run --rm cli chat "What is Python?"
docker-compose run --rm cli models list
```

---

### Step 6: Elasticsearch Heuristics & Cache
**Goal**: Implement prompt heuristics and similarity caching.

**Prompt File**: `prompts/06-elasticsearch-cache.md`

**Tasks**:
- Create Elasticsearch client
- Design heuristics index schema
- Design prompt cache index schema
- Implement prompt signature generation (NLP + hash)
- Implement cache lookup
- Implement heuristics storage
- Implement similarity search

**Index Schemas**:

**Heuristics Index**:
```json
{
  "mappings": {
    "properties": {
      "signature": {"type": "keyword"},
      "prompt": {"type": "text"},
      "behavior": {"type": "object"},
      "success_rate": {"type": "float"},
      "avg_tokens": {"type": "integer"},
      "timestamp": {"type": "date"},
      "model": {"type": "keyword"}
    }
  }
}
```

**Prompt Cache Index**:
```json
{
  "mappings": {
    "properties": {
      "signature": {"type": "keyword"},
      "prompt": {"type": "text"},
      "prompt_vector": {"type": "dense_vector", "dims": 384},
      "response": {"type": "text"},
      "timestamp": {"type": "date"},
      "model": {"type": "keyword"}
    }
  }
}
```

**Signature Generation**:
```python
# cli/src/cli/utils/prompt_signature.py
import hashlib
import spacy

nlp = spacy.load("en_core_web_sm")

def generate_signature(prompt: str, use_nlp: bool = True) -> str:
    """Generate prompt signature."""
    if use_nlp:
        doc = nlp(prompt)
        # Extract key features
        lemmas = [token.lemma_ for token in doc if not token.is_stop]
        normalized = " ".join(sorted(lemmas))
        return hashlib.sha256(normalized.encode()).hexdigest()
    else:
        return hashlib.sha256(prompt.encode()).hexdigest()
```

**Deliverables**:
- Elasticsearch client
- Index creation scripts
- Heuristics storage and retrieval
- Cache lookup and storage
- Similarity search implementation

**Validation**:
```bash
docker-compose run --rm cli cache status
docker-compose run --rm cli heuristics list
```

---

### Step 7: Redis Vector Store & Data Cache
**Goal**: Implement Redis for RAG and temporary data storage.

**Prompt File**: `prompts/07-redis-integration.md`

**Tasks**:
- Create Redis client with vector support
- Implement vector storage for RAG
- Implement DataFrame caching
- Implement session data storage
- Setup TTL for temporary data

**Key Implementation**:
```python
# cli/src/cli/services/redis_client.py
import redis
import pickle
import numpy as np

class RedisClient:
    def __init__(self, url: str):
        self.client = redis.from_url(url)
        
    def store_vector(self, key: str, vector: np.ndarray, metadata: dict):
        """Store vector with metadata for RAG."""
        self.client.hset(f"vector:{key}", mapping={
            "vector": pickle.dumps(vector),
            "metadata": pickle.dumps(metadata)
        })
        
    def store_dataframe(self, key: str, df, ttl: int = 3600):
        """Store DataFrame temporarily."""
        serialized = pickle.dumps(df)
        self.client.setex(f"df:{key}", ttl, serialized)
        
    def get_dataframe(self, key: str):
        """Retrieve DataFrame."""
        data = self.client.get(f"df:{key}")
        if data:
            return pickle.loads(data)
        return None
```

**Deliverables**:
- Redis client with vector support
- DataFrame caching
- Session management
- RAG vector storage

**Validation**:
```bash
docker-compose run --rm cli redis test
```

---

### Step 8: Sandbox Service & File Handling
**Goal**: Implement sandbox for temporary file processing.

**Prompt File**: `prompts/08-sandbox-service.md`

**Tasks**:
- Create sandbox Dockerfile
- Setup shared volume with CLI
- Implement file upload mechanism
- Implement file processing workflows
- Implement automatic cleanup
- Size limit enforcement

**Sandbox Dockerfile**:
```dockerfile
FROM alpine:latest

RUN apk add --no-cache \
    bash \
    curl

WORKDIR /workspace

# Keep container running
CMD ["tail", "-f", "/dev/null"]
```

**File Handler**:
```python
# cli/src/cli/utils/file_handler.py
import os
import shutil
from pathlib import Path

class FileHandler:
    def __init__(self, workspace: str = "/workspace", max_size: int = 100*1024*1024):
        self.workspace = Path(workspace)
        self.max_size = max_size
        
    def upload(self, file_path: str) -> str:
        """Upload file to sandbox."""
        file_size = os.path.getsize(file_path)
        if file_size > self.max_size:
            raise ValueError(f"File too large: {file_size} > {self.max_size}")
            
        dest = self.workspace / Path(file_path).name
        shutil.copy(file_path, dest)
        return str(dest)
        
    def cleanup(self, file_path: str):
        """Delete file from sandbox."""
        Path(file_path).unlink(missing_ok=True)
```

**Deliverables**:
- Sandbox service
- File upload/download
- Automatic cleanup
- Size validation

**Validation**:
```bash
docker-compose run --rm cli upload test.csv
docker-compose run --rm cli files list
docker-compose run --rm cli files cleanup
```

---

### Step 9: Data Analytics Integration
**Goal**: Integrate pandas, numpy, scikit-learn for data analytics.

**Prompt File**: `prompts/09-analytics-integration.md`

**Tasks**:
- Create analytics command module
- Implement CSV/Excel loading
- Implement basic statistics
- Implement visualization (text-based)
- Integration with Redis for caching
- PySpark bridge

**Analytics Command**:
```python
# cli/src/cli/commands/analyze.py
import click
import pandas as pd
from cli.services.redis_client import RedisClient

@click.command()
@click.argument('file_path')
@click.option('--cache-key', help='Cache result in Redis')
@click.pass_context
def analyze(ctx, file_path, cache_key):
    """Analyze data file."""
    # Load data
    df = pd.read_csv(file_path)
    
    # Basic statistics
    stats = df.describe()
    click.echo(stats)
    
    # Cache if requested
    if cache_key:
        redis = RedisClient(ctx.obj.redis_url)
        redis.store_dataframe(cache_key, df)
        click.echo(f"Cached as: {cache_key}")
```

**Deliverables**:
- Analytics command
- DataFrame operations
- Redis caching integration
- Basic statistics and reporting

**Validation**:
```bash
docker-compose run --rm cli analyze data.csv --cache-key my-data
docker-compose run --rm cli redis get-df my-data
```

---

### Step 10: Apache Spark Integration
**Goal**: Enable PySpark workflows from CLI.

**Prompt File**: `prompts/10-spark-integration.md`

**Tasks**:
- Create Spark client
- Implement job submission
- Implement result retrieval
- Example PySpark workflows
- Error handling

**Spark Client**:
```python
# cli/src/cli/services/spark_client.py
from pyspark.sql import SparkSession

class SparkClient:
    def __init__(self, master_url: str):
        self.spark = SparkSession.builder \
            .master(master_url) \
            .appName("VuhitraCLI") \
            .getOrCreate()
            
    def run_job(self, script_path: str):
        """Run PySpark job."""
        # Implementation
        pass
        
    def read_csv(self, path: str):
        """Read CSV with Spark."""
        return self.spark.read.csv(path, header=True)
```

**Deliverables**:
- Spark client
- Job submission
- Example workflows
- Integration with sandbox

**Validation**:
```bash
docker-compose run --rm cli spark submit job.py
docker-compose run --rm cli spark read data.csv
```

---

### Step 11: Dev Mode Implementation
**Goal**: Create iterative development mode with language separation.

**Prompt File**: `prompts/11-dev-mode.md`

**Tasks**:
- Create dev mode command
- Implement iteration loop
- Language-specific handlers (Python initially)
- File watching
- Auto-reload
- Error recovery

**Dev Mode Structure**:
```python
# cli/src/cli/commands/dev.py
import click
from cli.services.ollama_client import OllamaClient

@click.command()
@click.option('--language', default='python', type=click.Choice(['python', 'javascript', 'java']))
@click.option('--max-iterations', default=None, type=int)
@click.pass_context
def dev(ctx, language, max_iterations):
    """Start development mode."""
    max_iter = max_iterations or ctx.obj.max_iterations_dev
    
    click.echo(f"Dev mode: {language} (max {max_iter} iterations)")
    
    for i in range(max_iter):
        prompt = click.prompt(f"[{i+1}/{max_iter}] >>")
        
        if prompt.lower() == 'exit':
            break
            
        # Process with language-specific handler
        handler = get_language_handler(language)
        result = handler.process(prompt, ctx.obj)
        
        click.echo(result)
```

**Language Handler Interface**:
```python
# cli/src/cli/dev/base_handler.py
from abc import ABC, abstractmethod

class LanguageHandler(ABC):
    @abstractmethod
    def process(self, prompt: str, config) -> str:
        """Process prompt in language-specific context."""
        pass
        
    @abstractmethod
    def execute(self, code: str) -> str:
        """Execute generated code."""
        pass
```

**Deliverables**:
- Dev mode command
- Iteration framework
- Python language handler
- Extensible architecture for other languages

**Validation**:
```bash
docker-compose run --rm cli dev --language python
```

---

### Step 12: MCP Integration (stdio)
**Goal**: Add Model Context Protocol support for tool use.

**Prompt File**: `prompts/12-mcp-integration.md`

**Tasks**:
- Implement MCP client (stdio only)
- Tool discovery
- Tool execution
- Result handling
- Integration with OLLAMA

**MCP Client**:
```python
# cli/src/cli/services/mcp_client.py
import subprocess
import json

class MCPClient:
    def __init__(self, tool_path: str):
        self.tool_path = tool_path
        self.process = None
        
    def start(self):
        """Start MCP tool process."""
        self.process = subprocess.Popen(
            [self.tool_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call MCP tool."""
        message = json.dumps({
            "tool": tool_name,
            "arguments": arguments
        })
        
        self.process.stdin.write(message + "\n")
        self.process.stdin.flush()
        
        response = self.process.stdout.readline()
        return json.loads(response)
```

**Deliverables**:
- MCP client (stdio)
- Tool discovery and execution
- Integration with CLI commands

**Validation**:
```bash
docker-compose run --rm cli mcp list-tools
docker-compose run --rm cli mcp call tool_name --args '{}'
```

---

### Step 13: RAG Implementation
**Goal**: Implement Retrieval-Augmented Generation with Redis vectors.

**Prompt File**: `prompts/13-rag-implementation.md`

**Tasks**:
- Document ingestion
- Embedding generation via OLLAMA
- Vector storage in Redis
- Similarity search
- Context augmentation
- RAG query flow

**RAG Pipeline**:
```python
# cli/src/cli/rag/pipeline.py
class RAGPipeline:
    def __init__(self, ollama_client, redis_client):
        self.ollama = ollama_client
        self.redis = redis_client
        
    def ingest_document(self, text: str, doc_id: str):
        """Ingest document and create embeddings."""
        # Chunk document
        chunks = self.chunk_text(text)
        
        # Generate embeddings
        for i, chunk in enumerate(chunks):
            embedding = self.ollama.embed(chunk)
            self.redis.store_vector(
                f"{doc_id}:{i}",
                embedding,
                {"text": chunk, "doc_id": doc_id}
            )
            
    def query(self, question: str, top_k: int = 5) -> str:
        """Query with RAG."""
        # Get question embedding
        q_embedding = self.ollama.embed(question)
        
        # Find similar chunks
        similar = self.redis.search_vectors(q_embedding, top_k)
        
        # Build context
        context = "\n".join([s['metadata']['text'] for s in similar])
        
        # Augmented prompt
        prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        
        return self.ollama.generate(prompt)
```

**Deliverables**:
- RAG pipeline
- Document ingestion
- Vector search
- Query with context

**Validation**:
```bash
docker-compose run --rm cli rag ingest document.txt
docker-compose run --rm cli rag query "What is the main topic?"
```

---

### Step 14: NLP Enhancements (spaCy, VADER)
**Goal**: Add NLP capabilities for prompt analysis and sentiment.

**Prompt File**: `prompts/14-nlp-enhancements.md`

**Tasks**:
- Implement spaCy-based prompt analysis
- Implement VADER sentiment analysis
- Extract entities and intent
- Improve prompt signature generation
- Heuristic extraction

**NLP Analyzer**:
```python
# cli/src/cli/nlp/analyzer.py
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class PromptAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment = SentimentIntensityAnalyzer()
        
    def analyze(self, prompt: str) -> dict:
        """Analyze prompt with NLP."""
        doc = self.nlp(prompt)
        
        return {
            "entities": [(e.text, e.label_) for e in doc.ents],
            "sentiment": self.sentiment.polarity_scores(prompt),
            "intent": self.extract_intent(doc),
            "key_phrases": self.extract_key_phrases(doc)
        }
```

**Deliverables**:
- Prompt analysis
- Sentiment detection
- Entity extraction
- Intent classification

**Validation**:
```bash
docker-compose run --rm cli analyze-prompt "Can you help me with data analysis?"
```

---

### Step 15: Configuration & Environment Management
**Goal**: Finalize configuration management and validation.

**Prompt File**: `prompts/15-config-management.md`

**Tasks**:
- Create comprehensive .env.template
- Configuration validation
- Dynamic configuration updates
- Environment-specific configs
- Secrets management

**Configuration Files**:
- `.env.template` - Template with all parameters
- `.env.development` - Dev environment
- `.env.production` - Production environment
- `config/defaults.yaml` - Default values

**Deliverables**:
- Configuration templates
- Validation logic
- Documentation for all parameters

**Validation**:
```bash
docker-compose run --rm cli config validate
docker-compose run --rm cli config show
```

---

### Step 16: BuildKit Optimization
**Goal**: Optimize Docker builds with caching and multi-stage builds.

**Prompt File**: `prompts/16-buildkit-optimization.md`

**Tasks**:
- Configure BuildKit cache mounts
- Optimize layer ordering
- Implement multi-stage builds
- Cache APK packages
- Cache pip packages
- Minimize final image size

**Build Configuration**:
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with cache
docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1
```

**Deliverables**:
- Optimized Dockerfiles
- Build scripts
- Cache configuration
- Documentation

**Validation**:
```bash
# First build (downloads everything)
time docker-compose build

# Second build (uses cache)
time docker-compose build  # Should be much faster
```

---

### Step 17: Testing Infrastructure
**Goal**: Create comprehensive test suite.

**Prompt File**: `prompts/17-testing-infrastructure.md`

**Tasks**:
- Setup pytest
- Unit tests for all modules
- Integration tests for services
- End-to-end workflow tests
- Performance tests
- Test fixtures and mocks

**Test Structure**:
```
tests/
├── unit/
│   ├── test_config.py
│   ├── test_ollama_client.py
│   ├── test_redis_client.py
│   └── test_elastic_client.py
├── integration/
│   ├── test_cache_flow.py
│   ├── test_rag_pipeline.py
│   └── test_dev_mode.py
├── e2e/
│   └── test_workflows.py
└── conftest.py
```

**Deliverables**:
- Test suite
- Test configuration
- CI/CD integration
- Coverage reports

**Validation**:
```bash
docker-compose run --rm cli pytest
docker-compose run --rm cli pytest --cov=cli
```

---

### Step 18: Documentation & Examples
**Goal**: Create comprehensive documentation and example workflows.

**Prompt File**: `prompts/18-documentation.md`

**Tasks**:
- User guide
- API documentation
- Architecture diagrams
- Example workflows
- Troubleshooting guide
- Contributing guide

**Documentation Structure**:
```
docs/
├── user-guide/
│   ├── installation.md
│   ├── quick-start.md
│   └── commands.md
├── architecture/
│   ├── overview.md
│   ├── services.md
│   └── diagrams/
├── examples/
│   ├── data-analytics.md
│   ├── rag-qa.md
│   └── dev-mode.md
└── troubleshooting.md
```

**Example Workflows**:
```
examples/
├── 01-simple-chat/
├── 02-data-analysis/
├── 03-rag-qa/
├── 04-pyspark-job/
└── 05-dev-mode-python/
```

**Deliverables**:
- Complete documentation
- Working examples
- Video tutorials (optional)

**Validation**:
- All examples run successfully
- Documentation is clear and accurate

---

### Step 19: Security & Performance Hardening
**Goal**: Security audit and performance optimization.

**Prompt File**: `prompts/19-security-hardening.md`

**Tasks**:
- Security audit
- Input validation
- Resource limits
- Performance profiling
- Optimization
- Security best practices

**Security Checklist**:
- [ ] Input sanitization
- [ ] File size limits enforced
- [ ] No hardcoded secrets
- [ ] Proper error handling
- [ ] Container security
- [ ] Network isolation
- [ ] Volume permissions

**Deliverables**:
- Security audit report
- Performance benchmarks
- Optimization recommendations

**Validation**:
```bash
docker-compose run --rm cli security-check
docker-compose run --rm cli benchmark
```

---

### Step 20: Final Integration & Release Preparation
**Goal**: Final testing, integration, and release preparation.

**Prompt File**: `prompts/20-final-integration.md`

**Tasks**:
- Full system integration test
- Documentation review
- Version tagging
- Release notes
- Docker Hub publishing
- GitHub release

**Pre-release Checklist**:
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Examples working
- [ ] Security audit passed
- [ ] Performance acceptable
- [ ] README updated
- [ ] CHANGELOG created
- [ ] Version tagged

**Deliverables**:
- Release v0.1.0
- Published Docker images
- Release announcement

**Validation**:
```bash
# Full system test
./scripts/full-system-test.sh

# Version check
docker-compose run --rm cli --version  # Should show 0.1.0
```

---

## Testing Strategy

### Unit Testing
- Test individual modules in isolation
- Mock external dependencies
- Achieve >80% code coverage

### Integration Testing
- Test service interactions
- Redis, Elasticsearch, OLLAMA integration
- End-to-end command flows

### Performance Testing
- Load testing with multiple concurrent requests
- Memory usage monitoring
- Response time benchmarks

### Security Testing
- Input validation tests
- File upload security
- Container security scanning

## Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check logs
docker-compose logs -f [service-name]

# Check health
docker-compose ps
```

#### OLLAMA Connection Failed
```bash
# Verify OLLAMA is running
curl http://localhost:11434/api/tags

# Check environment variable
docker-compose run --rm cli env | grep OLLAMA_IP
```

#### Elasticsearch Not Healthy
```bash
# Check Elasticsearch logs
docker-compose logs elasticsearch

# Verify cluster health
curl http://localhost:9200/_cluster/health
```

#### BuildKit Cache Issues
```bash
# Clear build cache
docker builder prune

# Rebuild without cache
docker-compose build --no-cache
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
docker-compose up
```

## Next Steps After Implementation

1. **Community Feedback**: Gather user feedback
2. **Feature Requests**: Prioritize new features
3. **Performance Tuning**: Optimize based on real usage
4. **Additional Languages**: Add JavaScript, Java support to dev mode
5. **Web UI**: Consider web interface
6. **Plugin System**: Allow community extensions

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Security patches as needed
- Model updates (new OLLAMA models)
- Documentation updates
- Community support

### Monitoring
- Resource usage
- Error rates
- Cache hit rates
- Performance metrics

---

**Document Version**: 1.0
**Last Updated**: 2025-11-06
**Status**: Ready for Implementation
