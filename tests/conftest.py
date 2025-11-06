# Pytest Configuration and Fixtures

import pytest
import os
from pathlib import Path


# Configure test paths
@pytest.fixture(scope="session")
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def config_dir():
    """Return path to config directory."""
    return Path(__file__).parent.parent / "config"


# Mock service clients for unit tests
@pytest.fixture
def mock_redis_client(mocker):
    """Mock Redis client for unit tests."""
    return mocker.MagicMock()


@pytest.fixture
def mock_elasticsearch_client(mocker):
    """Mock Elasticsearch client for unit tests."""
    return mocker.MagicMock()


@pytest.fixture
def mock_ollama_client(mocker):
    """Mock OLLAMA client for unit tests."""
    return mocker.MagicMock()


@pytest.fixture
def mock_spark_client(mocker):
    """Mock Spark client for unit tests."""
    return mocker.MagicMock()


# Environment configuration for tests
@pytest.fixture(scope="session", autouse=True)
def test_environment():
    """Set up test environment variables."""
    os.environ.setdefault("OLLAMA_IP", "http://localhost:11434")
    os.environ.setdefault("MODEL", "llama3:8b")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
    os.environ.setdefault("ELASTICSEARCH_URL", "http://localhost:9200")
    os.environ.setdefault("LOG_LEVEL", "DEBUG")
    yield
    # Cleanup if needed


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
