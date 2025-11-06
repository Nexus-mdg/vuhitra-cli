# Step 2: Docker Compose Foundation

## Objective
Create the base docker-compose.yml file with all required services properly configured.

## Context
Vuhitra CLI requires 5 services running in containers: CLI, Redis, Elasticsearch, Apache Spark, and Sandbox. This step establishes the orchestration layer that brings all services together.

## Requirements

### Services Overview

1. **CLI Service**
   - Build from ./cli directory
   - Depends on: redis, elasticsearch, spark
   - Shared volume with sandbox
   - Environment variables from .env
   - Interactive mode capable (stdin_open, tty)

2. **Redis Service (>= 7.2)**
   - Image: redis:7.2-alpine
   - Port: 6379 (internal)
   - Persistent volume for data
   - Health check using redis-cli ping
   - Optional: custom redis.conf

3. **Elasticsearch Service (8.11.x)**
   - Image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
   - Port: 9200 (internal)
   - Single-node setup (discovery.type=single-node)
   - Disable xpack.security for development
   - Memory limits (e.g., -Xms512m -Xmx512m)
   - Health check using cluster health API
   - Persistent volume for data

4. **Apache Spark Service**
   - Image: ghcr.io/nexus-mdg/spark-3.5:latest
   - Master mode
   - Port: 7077 (internal)
   - Web UI: 8080 (optional exposure)
   - Resource configuration via environment

5. **Sandbox Service**
   - Build from ./docker/sandbox
   - Minimal Alpine-based container
   - Shared workspace volume with CLI
   - Keep-alive command (tail -f /dev/null)
   - No persistent data

### Network Configuration
- Create custom bridge network: vuhitra-network
- All services on same network
- Internal DNS resolution by service name

### Volume Configuration
- **redis-data**: Persistent Redis data
- **elasticsearch-data**: Persistent Elasticsearch indices
- **sandbox-workspace**: Shared workspace (tmpfs or named volume)
- **cli-cache**: Optional pip/apk cache for builds

### Environment Variables (.env.template)
Create template with all configurable parameters:

```env
# OLLAMA Configuration
OLLAMA_IP=http://host.docker.internal:11434
MODEL=llama3:8b

# File Size Limits (bytes)
MAX_CONTEXT_FILE_SIZE=10485760
MAX_UPLOADED_FILE_SIZE=104857600

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

# Elasticsearch
ES_JAVA_OPTS=-Xms512m -Xmx512m

# Spark
SPARK_WORKER_MEMORY=2g
SPARK_WORKER_CORES=2
```

## docker-compose.yml Structure

```yaml
version: '3.8'

services:
  cli:
    build:
      context: ./cli
      dockerfile: Dockerfile
      args:
        BUILDKIT_INLINE_CACHE: 1
    image: vuhitra-cli:latest
    container_name: vuhitra-cli
    stdin_open: true
    tty: true
    volumes:
      - ./cli/src:/app/src  # Development mount
      - sandbox-workspace:/workspace
      - cli-cache:/root/.cache  # Build cache
    environment:
      - OLLAMA_IP=${OLLAMA_IP}
      - MODEL=${MODEL}
      - MAX_CONTEXT_FILE_SIZE=${MAX_CONTEXT_FILE_SIZE}
      - MAX_UPLOADED_FILE_SIZE=${MAX_UPLOADED_FILE_SIZE}
      - MAX_ITERATIONS_DEV=${MAX_ITERATIONS_DEV}
      - MAX_ITERATIONS_PROD=${MAX_ITERATIONS_PROD}
      - ENABLE_PROMPT_CACHE=${ENABLE_PROMPT_CACHE}
      - ENABLE_HEURISTICS=${ENABLE_HEURISTICS}
      - REDIS_URL=${REDIS_URL}
      - ELASTICSEARCH_URL=${ELASTICSEARCH_URL}
      - SPARK_MASTER=${SPARK_MASTER}
      - LOG_LEVEL=${LOG_LEVEL}
    depends_on:
      redis:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
      spark:
        condition: service_started
    networks:
      - vuhitra-network
    command: tail -f /dev/null  # Keep container running for development

  redis:
    image: redis:7.2-alpine
    container_name: vuhitra-redis
    ports:
      - "6379"  # Internal only
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - vuhitra-network
    restart: unless-stopped

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: vuhitra-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=${ES_JAVA_OPTS}"
    ports:
      - "9200"  # Internal only
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    networks:
      - vuhitra-network
    restart: unless-stopped

  spark:
    image: ghcr.io/nexus-mdg/spark-3.5:latest
    container_name: vuhitra-spark
    environment:
      - SPARK_MODE=master
      - SPARK_WORKER_MEMORY=${SPARK_WORKER_MEMORY:-2g}
      - SPARK_WORKER_CORES=${SPARK_WORKER_CORES:-2}
    ports:
      - "7077"  # Internal only
      - "8080"  # Web UI (optional exposure)
    networks:
      - vuhitra-network
    restart: unless-stopped

  sandbox:
    build:
      context: ./docker/sandbox
      dockerfile: Dockerfile
    image: vuhitra-sandbox:latest
    container_name: vuhitra-sandbox
    volumes:
      - sandbox-workspace:/workspace
    networks:
      - vuhitra-network
    command: tail -f /dev/null
    restart: unless-stopped

networks:
  vuhitra-network:
    driver: bridge

volumes:
  redis-data:
    driver: local
  elasticsearch-data:
    driver: local
  sandbox-workspace:
    driver: local
  cli-cache:
    driver: local
```

## Tasks

1. **Create docker-compose.yml**
   - Define all 5 services
   - Configure dependencies
   - Setup health checks
   - Configure volumes and networks

2. **Create .env.template**
   - Include all configuration parameters
   - Add comments explaining each parameter
   - Provide sensible defaults

3. **Create .env from template**
   - Copy .env.template to .env
   - This file should be in .gitignore
   - Users will customize this file

4. **Test configuration**
   - Validate YAML syntax: `docker-compose config`
   - Check service definitions
   - Verify environment variable interpolation

## Expected Output

After completion:
- docker-compose.yml with all 5 services
- .env.template with all parameters documented
- .env file for local development
- Services configured with proper dependencies
- Health checks in place
- Networks and volumes defined

## Validation Steps

1. **Validate syntax**:
   ```bash
   docker-compose config
   ```

2. **Check service definitions**:
   ```bash
   docker-compose config --services
   # Should output: cli, redis, elasticsearch, spark, sandbox
   ```

3. **Verify environment variables**:
   ```bash
   docker-compose config | grep OLLAMA_IP
   ```

4. **Attempt to pull images** (don't start yet):
   ```bash
   docker-compose pull redis elasticsearch spark
   ```

## Notes

- Don't start services yet (builds not ready)
- Ensure Docker and Docker Compose are up to date
- Document any port exposures for debugging
- Consider resource limits for production

## Next Step
Proceed to Step 3: CLI Dockerfile with BuildKit Optimization
