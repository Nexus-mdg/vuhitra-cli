# Examples

This directory contains example workflows and use cases for Vuhitra CLI.

## Directory Structure

Each example is organized in its own subdirectory with:
- README.md - Description and instructions
- Sample code/scripts
- Sample data (if applicable)
- Expected output

## Planned Examples

The following examples will be added during implementation:

### `01-simple-chat/`
Basic chat interaction with AI models
- Simple prompts and responses
- Model selection
- Streaming responses

### `02-data-analysis/`
Data analytics workflows
- CSV/Excel file analysis
- Statistical operations
- Data visualization
- Caching results in Redis

### `03-rag-qa/`
Retrieval-Augmented Generation for Q&A
- Document ingestion
- Vector storage
- Question answering with context
- Similarity search

### `04-pyspark-job/`
Apache Spark integration examples
- PySpark job submission
- Distributed data processing
- Results retrieval

### `05-dev-mode-python/`
Development mode for iterative coding
- Python code generation
- Iterative refinement
- Error handling and debugging

## Running Examples

Each example directory contains a README with specific instructions. General steps:

1. Ensure all services are running:
   ```bash
   docker-compose up -d
   ```

2. Navigate to the example directory:
   ```bash
   cd examples/01-simple-chat/
   ```

3. Follow the README instructions in that directory

## Contributing Examples

When adding new examples:
- Create a new directory with a descriptive name
- Include a comprehensive README
- Add sample data if needed (keep files small)
- Test the example thoroughly
- Document expected output
