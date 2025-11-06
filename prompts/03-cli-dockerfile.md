# Step 3: CLI Dockerfile with BuildKit Optimization

## Objective
Create an optimized Dockerfile for the CLI service with BuildKit caching for APK and pip packages.

## Context
The CLI service is the core of Vuhitra CLI. It needs Python 3.11+, NLP libraries (spaCy, VADER), data analytics libraries (pandas, numpy, scikit-learn), and OLLAMA client. BuildKit optimization will speed up rebuilds significantly.

## Requirements

### Base Image
- Python 3.11 on Alpine Linux (python:3.11-alpine)
- Alpine for smaller image size
- Multi-stage build for optimization

### System Dependencies
Required APK packages:
- gcc, g++ (compilation)
- musl-dev (Alpine C library)
- linux-headers (kernel headers)
- libffi-dev (foreign function interface)
- openssl-dev (SSL support)
- postgresql-dev (if needed for future DB support)
- curl, bash (utilities)

### Python Dependencies (requirements.txt)
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
redis[hiredis]>=5.0.0
elasticsearch>=8.11.0

# Spark
pyspark>=3.5.0

# Utilities
python-dotenv>=1.0.0
click>=8.1.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
requests>=2.31.0

# Development
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
flake8>=6.1.0
mypy>=1.5.0
```

### spaCy Models
- en_core_web_sm (small English model)
- Download during build

### BuildKit Features
- Cache mount for /var/cache/apk (APK cache)
- Cache mount for /root/.cache/pip (pip cache)
- Multi-stage build to minimize final image
- Layer optimization (COPY in correct order)

## Dockerfile Structure

```dockerfile
# syntax=docker/dockerfile:1.4

#################
# Stage 1: Base #
#################
FROM python:3.11-alpine AS base

# Install system dependencies with cache mount
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    linux-headers \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

#########################
# Stage 2: Dependencies #
#########################
FROM base AS dependencies

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages with cache mount
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

#####################
# Stage 3: Builder  #
#####################
FROM dependencies AS builder

# Copy application code
COPY src/ ./src/

# Compile Python files
RUN python -m compileall src/

##################
# Stage 4: Final #
##################
FROM python:3.11-alpine AS final

# Install only runtime dependencies (no build tools)
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache \
    bash \
    curl \
    libpq \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copy Python packages from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application code from builder
COPY --from=builder /app/src ./src

# Create non-root user
RUN addgroup -g 1000 vuhitra && \
    adduser -D -u 1000 -G vuhitra vuhitra && \
    chown -R vuhitra:vuhitra /app

USER vuhitra

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/home/vuhitra/.local/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import cli; print('OK')" || exit 1

# Default command (can be overridden)
ENTRYPOINT ["python", "-m", "cli.main"]
CMD ["--help"]
```

## requirements.txt Details

Create comprehensive requirements.txt with version pinning:

```txt
# Core AI/ML
ollama==0.1.5

# NLP Libraries
spacy==3.7.2
vaderSentiment==3.3.2

# Data Science Stack
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
scipy==1.11.4

# Database and Cache
redis[hiredis]==5.0.1
elasticsearch==8.11.1

# Apache Spark
pyspark==3.5.0

# Web and HTTP
requests==2.31.0
urllib3==2.1.0

# Configuration and CLI
python-dotenv==1.0.0
click==8.1.7
pydantic==2.5.2
pydantic-settings==2.1.0

# Utilities
python-json-logger==2.0.7
colorama==0.4.6

# Development and Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
black==23.12.1
flake8==6.1.0
mypy==1.7.1
isort==5.13.2

# Type stubs
types-requests==2.31.0.10
```

## .dockerignore

Create .dockerignore to reduce build context:

```
# Git
.git/
.gitignore
.gitattributes

# Documentation
README.md
docs/
*.md

# Tests
tests/
.pytest_cache/
.coverage
htmlcov/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# CI/CD
.github/

# Environment
.env
.env.local

# Examples
examples/
```

## Build Script

Create `scripts/build-cli.sh`:

```bash
#!/bin/bash
set -e

echo "Building Vuhitra CLI with BuildKit..."

# Enable BuildKit
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Build with cache
docker build \
    --progress=plain \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    -t vuhitra-cli:latest \
    -f cli/Dockerfile \
    ./cli

echo "Build complete!"
```

## Tasks

1. **Create cli/Dockerfile**
   - Implement multi-stage build
   - Add BuildKit cache mounts
   - Optimize layer ordering
   - Include health check

2. **Create cli/requirements.txt**
   - List all dependencies
   - Pin versions for reproducibility
   - Add comments for clarity

3. **Create cli/.dockerignore**
   - Exclude unnecessary files
   - Reduce build context size

4. **Create placeholder Python structure**
   ```
   cli/src/
   └── cli/
       ├── __init__.py
       └── main.py (placeholder)
   ```

5. **Create build script**
   - scripts/build-cli.sh
   - Make executable

## Expected Output

After completion:
- Optimized multi-stage Dockerfile
- Comprehensive requirements.txt
- Efficient .dockerignore
- Basic Python package structure
- Build script for easy building

## Validation Steps

1. **Validate Dockerfile syntax**:
   ```bash
   docker build --check ./cli
   ```

2. **Build the image** (first time, downloads everything):
   ```bash
   time DOCKER_BUILDKIT=1 docker build -t vuhitra-cli:test ./cli
   ```

3. **Rebuild** (should use cache):
   ```bash
   time DOCKER_BUILDKIT=1 docker build -t vuhitra-cli:test ./cli
   # Should be much faster
   ```

4. **Check image size**:
   ```bash
   docker images vuhitra-cli:test
   # Should be reasonable (< 1GB)
   ```

5. **Run container**:
   ```bash
   docker run --rm vuhitra-cli:test --help
   # Should show help message
   ```

6. **Verify libraries**:
   ```bash
   docker run --rm vuhitra-cli:test python -c "import pandas, numpy, spacy, redis, elasticsearch; print('All imports successful')"
   ```

## Notes

- BuildKit must be enabled
- First build will take longer (downloading)
- Subsequent builds use cache effectively
- Multi-stage keeps final image small
- Non-root user for security

## Next Step
Proceed to Step 4: CLI Core Application Structure
