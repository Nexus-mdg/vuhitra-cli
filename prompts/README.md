# Implementation Prompts

This directory contains detailed prompts for each implementation step of the Vuhitra CLI project.

## Overview

Each prompt file corresponds to a step in the `IMPLEMENTATION.md` guide and provides:
- Detailed objectives
- Context and requirements
- Implementation guidelines
- Validation steps
- Next step reference

## Prompt Files

| Step | File | Description |
|------|------|-------------|
| 01 | [01-project-structure.md](01-project-structure.md) | Project structure setup |
| 02 | [02-docker-compose.md](02-docker-compose.md) | Docker Compose foundation |
| 03 | [03-cli-dockerfile.md](03-cli-dockerfile.md) | CLI Dockerfile with BuildKit |
| 04 | [04-cli-core.md](04-cli-core.md) | CLI core application structure |
| 05 | [05-ollama-integration.md](05-ollama-integration.md) | OLLAMA integration |
| 06 | [06-elasticsearch-cache.md](06-elasticsearch-cache.md) | Elasticsearch heuristics & cache |
| 07 | [07-redis-integration.md](07-redis-integration.md) | Redis vector store & data cache |
| 08 | [08-sandbox-service--file-handling.md](08-sandbox-service--file-handling.md) | Sandbox service & file handling |
| 09 | [09-data-analytics-integration.md](09-data-analytics-integration.md) | Data analytics integration |
| 10 | [10-apache-spark-integration.md](10-apache-spark-integration.md) | Apache Spark integration |
| 11 | [11-dev-mode-implementation.md](11-dev-mode-implementation.md) | Dev mode implementation |
| 12 | [12-mcp-integration-stdio.md](12-mcp-integration-stdio.md) | MCP integration (stdio) |
| 13 | [13-rag-implementation.md](13-rag-implementation.md) | RAG implementation |
| 14 | [14-nlp-enhancements-spacy-vader.md](14-nlp-enhancements-spacy-vader.md) | NLP enhancements |
| 15 | [15-configuration--environment-management.md](15-configuration--environment-management.md) | Configuration management |
| 16 | [16-buildkit-optimization.md](16-buildkit-optimization.md) | BuildKit optimization |
| 17 | [17-testing-infrastructure.md](17-testing-infrastructure.md) | Testing infrastructure |
| 18 | [18-documentation--examples.md](18-documentation--examples.md) | Documentation & examples |
| 19 | [19-security--performance-hardening.md](19-security--performance-hardening.md) | Security & performance |
| 20 | [20-final-integration--release-preparation.md](20-final-integration--release-preparation.md) | Final integration & release |

## Usage

1. **Read the main guides first**:
   - Start with `TODO.md` for project overview
   - Review `IMPLEMENTATION.md` for complete implementation plan

2. **Follow steps sequentially**:
   - Each step builds on previous steps
   - Complete validation before moving to next step
   - Reference IMPLEMENTATION.md for detailed requirements

3. **Use prompts for AI assistance**:
   - Copy prompt content when requesting AI help
   - Provide context from previous steps
   - Include validation results

## Implementation Workflow

```
TODO.md (Project Overview)
    ↓
IMPLEMENTATION.md (Complete Guide)
    ↓
prompts/01-*.md → prompts/02-*.md → ... → prompts/20-*.md
    ↓                     ↓                        ↓
  Step 1              Step 2                   Step 20
    ↓                     ↓                        ↓
Validation          Validation               Final Release
```

## Notes

- Steps 1-5: Foundation (Docker, CLI core, OLLAMA)
- Steps 6-10: Data layer (Elasticsearch, Redis, Spark)
- Steps 11-14: Advanced features (Dev mode, MCP, RAG, NLP)
- Steps 15-17: Infrastructure (Config, optimization, testing)
- Steps 18-20: Polish (Docs, security, release)

## Contributing

When adding new steps:
1. Follow the existing prompt format
2. Include clear objectives and validation
3. Reference IMPLEMENTATION.md
4. Update this README

---

**Last Updated**: 2025-11-06
