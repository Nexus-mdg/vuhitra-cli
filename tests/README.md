# Tests

This directory contains all tests for the Vuhitra CLI project.

## Directory Structure

### `unit/`
Unit tests for individual modules and functions:
- Test one component in isolation
- Mock external dependencies
- Fast execution
- High coverage target (>80%)

### `integration/`
Integration tests for service interactions:
- Test multiple components together
- Verify service communication (Redis, Elasticsearch, OLLAMA)
- Test end-to-end command flows
- Require services to be running

### `e2e/`
End-to-end tests for complete workflows:
- Test full user workflows
- Validate complete features
- Test real-world scenarios
- May require all services running

## Running Tests

### Prerequisites
Ensure Docker and Docker Compose are installed and services are running:
```bash
docker-compose up -d
```

### Run All Tests
```bash
docker-compose run --rm cli pytest
```

### Run Specific Test Suite
```bash
# Unit tests only
docker-compose run --rm cli pytest tests/unit/

# Integration tests only
docker-compose run --rm cli pytest tests/integration/

# E2E tests only
docker-compose run --rm cli pytest tests/e2e/
```

### Run Specific Test File
```bash
docker-compose run --rm cli pytest tests/unit/test_config.py
```

### With Coverage Report
```bash
docker-compose run --rm cli pytest --cov=cli --cov-report=html
```

## Test Configuration

Test configuration is managed in `conftest.py` which includes:
- Pytest fixtures
- Mock configurations
- Test data setup
- Shared utilities

## Writing Tests

### Unit Test Example
```python
# tests/unit/test_config.py
import pytest
from cli.config import Config

def test_config_defaults():
    config = Config()
    assert config.model == "llama3:8b"
    assert config.max_iterations_dev == 50
```

### Integration Test Example
```python
# tests/integration/test_redis_client.py
import pytest
from cli.services.redis_client import RedisClient

@pytest.fixture
def redis_client():
    return RedisClient("redis://redis:6379")

def test_redis_connection(redis_client):
    assert redis_client.ping()
```

## Test Standards

- Use pytest framework
- Follow AAA pattern (Arrange, Act, Assert)
- Clear test names describing what is tested
- One assertion per test when possible
- Proper cleanup in teardown
- Mock external dependencies in unit tests
- Use fixtures for common setup

## Coverage Goals

- Unit tests: >80% coverage
- Integration tests: Cover all service interactions
- E2E tests: Cover main user workflows

## CI/CD Integration

Tests are automatically run in CI/CD pipeline:
- On every pull request
- On commits to main branch
- Coverage reports generated
- Failed tests block merges

## Troubleshooting

### Tests Hang or Timeout
- Check if required services are running
- Verify network connectivity between containers
- Check service health: `docker-compose ps`

### Import Errors
- Ensure CLI package is properly installed
- Check PYTHONPATH in test environment
- Verify Docker volumes are mounted correctly

### Flaky Tests
- Check for race conditions
- Ensure proper cleanup between tests
- Verify service readiness before running tests
