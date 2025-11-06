# Step 4: CLI Core Application Structure

## Objective
Implement the basic CLI application framework with configuration management, logging, and command routing.

## Context
Create the foundation of the CLI application using Click for command-line interface, Pydantic for configuration, and proper Python package structure.

## Requirements

### Package Structure
```
cli/src/
└── cli/
    ├── __init__.py
    ├── main.py              # CLI entry point with Click
    ├── config.py            # Pydantic configuration
    ├── logger.py            # Logging configuration
    ├── commands/            # CLI command modules
    │   ├── __init__.py
    │   ├── chat.py         # Chat with AI
    │   ├── analyze.py      # Data analysis
    │   ├── dev.py          # Dev mode
    │   ├── cache.py        # Cache management
    │   └── config_cmd.py   # Config commands
    ├── services/            # External service clients
    │   ├── __init__.py
    │   ├── ollama_client.py
    │   ├── redis_client.py
    │   ├── elastic_client.py
    │   └── spark_client.py
    └── utils/               # Utilities
        ├── __init__.py
        ├── prompt_signature.py
        └── file_handler.py
```

### Core Components

#### 1. cli/__init__.py
```python
"""Vuhitra CLI - AI-powered data analytics and development."""

__version__ = "0.1.0"
__author__ = "Nexus-mdg"
__license__ = "MIT"
```

#### 2. cli/config.py
```python
"""Configuration management using Pydantic."""

from pydantic_settings import BaseSettings
from typing import Optional


class Config(BaseSettings):
    """Application configuration."""
    
    # OLLAMA Configuration
    ollama_ip: str = "http://ollama:11434"
    model: str = "llama3:8b"
    
    # File Size Limits (in bytes)
    max_context_file_size: int = 10 * 1024 * 1024  # 10MB
    max_uploaded_file_size: int = 100 * 1024 * 1024  # 100MB
    
    # Iteration Limits
    max_iterations_dev: int = 50
    max_iterations_prod: int = 5
    
    # Feature Flags
    enable_prompt_cache: bool = False
    enable_heuristics: bool = True
    
    # Service URLs
    redis_url: str = "redis://redis:6379"
    elasticsearch_url: str = "http://elasticsearch:9200"
    spark_master: str = "spark://spark:7077"
    
    # Logging
    log_level: str = "INFO"
    
    # Workspace
    workspace_path: str = "/workspace"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
```

#### 3. cli/logger.py
```python
"""Logging configuration."""

import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(log_level: str = "INFO") -> logging.Logger:
    """Setup application logger."""
    
    # Create logger
    logger = logging.getLogger("vuhitra")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with JSON formatting
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str = "vuhitra") -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name)
```

#### 4. cli/main.py
```python
"""Main CLI entry point."""

import click
import sys
from cli import __version__
from cli.config import get_config
from cli.logger import setup_logger, get_logger


# Import command groups
from cli.commands import chat, analyze, dev, cache, config_cmd


@click.group()
@click.version_option(version=__version__, prog_name="vuhitra")
@click.option('--log-level', default=None, help='Set logging level')
@click.pass_context
def cli(ctx, log_level):
    """Vuhitra CLI - AI-powered data analytics and development.
    
    A Docker-based CLI tool leveraging OLLAMA models for intelligent
    data processing, code generation, and development workflows.
    """
    # Initialize context
    ctx.ensure_object(dict)
    
    # Load configuration
    config = get_config()
    if log_level:
        config.log_level = log_level
    ctx.obj['config'] = config
    
    # Setup logging
    logger = setup_logger(config.log_level)
    ctx.obj['logger'] = logger
    
    logger.info("Vuhitra CLI started", extra={
        "version": __version__,
        "log_level": config.log_level
    })


# Register command groups
cli.add_command(chat.chat)
cli.add_command(analyze.analyze)
cli.add_command(dev.dev)
cli.add_command(cache.cache_group)
cli.add_command(config_cmd.config_group)


@cli.command()
def version():
    """Show version information."""
    click.echo(f"Vuhitra CLI v{__version__}")
    click.echo("Copyright (c) 2025 Nexus-mdg")
    click.echo("License: MIT")


@cli.command()
@click.pass_context
def info(ctx):
    """Show configuration and system information."""
    config = ctx.obj['config']
    
    click.echo("=== Vuhitra CLI Information ===")
    click.echo(f"Version: {__version__}")
    click.echo(f"\n=== Configuration ===")
    click.echo(f"OLLAMA IP: {config.ollama_ip}")
    click.echo(f"Model: {config.model}")
    click.echo(f"Redis URL: {config.redis_url}")
    click.echo(f"Elasticsearch URL: {config.elasticsearch_url}")
    click.echo(f"Spark Master: {config.spark_master}")
    click.echo(f"\n=== Features ===")
    click.echo(f"Prompt Cache: {'Enabled' if config.enable_prompt_cache else 'Disabled'}")
    click.echo(f"Heuristics: {'Enabled' if config.enable_heuristics else 'Disabled'}")


def main():
    """Entry point for the CLI."""
    try:
        cli(obj={})
    except Exception as e:
        logger = get_logger()
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
```

#### 5. Command Stubs

Create placeholder command modules:

**cli/commands/__init__.py**:
```python
"""CLI command modules."""
```

**cli/commands/chat.py**:
```python
"""Chat command - interact with AI models."""

import click


@click.command()
@click.argument('prompt', required=False)
@click.option('--stream', is_flag=True, help='Stream response')
@click.pass_context
def chat(ctx, prompt, stream):
    """Chat with AI model.
    
    Examples:
        vuhitra chat "What is Python?"
        vuhitra chat --stream "Explain machine learning"
    """
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    if not prompt:
        prompt = click.prompt("Enter your prompt")
    
    logger.info(f"Chat request", extra={"prompt": prompt[:50]})
    
    # TODO: Implement OLLAMA integration
    click.echo(f"[Chat mode - Not yet implemented]")
    click.echo(f"Prompt: {prompt}")
    click.echo(f"Model: {config.model}")
    click.echo(f"Stream: {stream}")
```

**cli/commands/analyze.py**:
```python
"""Data analysis commands."""

import click


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--cache-key', help='Store result in cache')
@click.pass_context
def analyze(ctx, file_path, cache_key):
    """Analyze data file.
    
    Examples:
        vuhitra analyze data.csv
        vuhitra analyze data.csv --cache-key my-analysis
    """
    logger = ctx.obj['logger']
    
    logger.info(f"Analyze request", extra={"file": file_path})
    
    # TODO: Implement data analysis
    click.echo(f"[Analyze mode - Not yet implemented]")
    click.echo(f"File: {file_path}")
```

**cli/commands/dev.py**:
```python
"""Development mode commands."""

import click


@click.command()
@click.option('--language', default='python', type=click.Choice(['python', 'javascript', 'java']))
@click.option('--max-iterations', type=int, help='Override max iterations')
@click.pass_context
def dev(ctx, language, max_iterations):
    """Start development mode.
    
    Examples:
        vuhitra dev --language python
        vuhitra dev --language python --max-iterations 100
    """
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    max_iter = max_iterations or config.max_iterations_dev
    
    logger.info(f"Dev mode started", extra={
        "language": language,
        "max_iterations": max_iter
    })
    
    # TODO: Implement dev mode
    click.echo(f"[Dev mode - Not yet implemented]")
    click.echo(f"Language: {language}")
    click.echo(f"Max iterations: {max_iter}")
```

**cli/commands/cache.py**:
```python
"""Cache management commands."""

import click


@click.group(name='cache')
def cache_group():
    """Manage prompt cache and heuristics."""
    pass


@cache_group.command(name='status')
@click.pass_context
def cache_status(ctx):
    """Show cache status."""
    # TODO: Implement cache status
    click.echo("[Cache status - Not yet implemented]")


@cache_group.command(name='clear')
@click.pass_context
def cache_clear(ctx):
    """Clear cache."""
    # TODO: Implement cache clear
    click.echo("[Cache clear - Not yet implemented]")
```

**cli/commands/config_cmd.py**:
```python
"""Configuration commands."""

import click


@click.group(name='config')
def config_group():
    """Manage configuration."""
    pass


@config_group.command(name='show')
@click.pass_context
def config_show(ctx):
    """Show current configuration."""
    config = ctx.obj['config']
    
    click.echo("=== Configuration ===")
    for key, value in config.model_dump().items():
        click.echo(f"{key}: {value}")


@config_group.command(name='validate')
@click.pass_context
def config_validate(ctx):
    """Validate configuration."""
    config = ctx.obj['config']
    
    try:
        # TODO: Add validation logic
        click.echo("✓ Configuration is valid")
    except Exception as e:
        click.echo(f"✗ Configuration error: {str(e)}", err=True)
```

## Tasks

1. **Create package structure**
   - All directories and __init__.py files
   - Proper Python package organization

2. **Implement core modules**
   - config.py with Pydantic
   - logger.py with JSON formatting
   - main.py with Click

3. **Create command stubs**
   - All command modules as placeholders
   - Proper Click decorators
   - Help text and examples

4. **Create service client stubs**
   - Empty files for now
   - Will be implemented in later steps

5. **Update pyproject.toml** (optional)
   - Package metadata
   - Entry points

## Expected Output

After completion:
- Complete CLI package structure
- Working CLI with help system
- Configuration management
- Logging setup
- Command stubs ready for implementation

## Validation Steps

1. **Test basic CLI**:
   ```bash
   docker-compose run --rm cli --help
   docker-compose run --rm cli --version
   docker-compose run --rm cli info
   ```

2. **Test commands**:
   ```bash
   docker-compose run --rm cli chat --help
   docker-compose run --rm cli analyze --help
   docker-compose run --rm cli dev --help
   docker-compose run --rm cli cache --help
   docker-compose run --rm cli config show
   ```

3. **Test configuration**:
   ```bash
   docker-compose run --rm cli config show
   docker-compose run --rm cli info
   ```

4. **Verify imports**:
   ```bash
   docker-compose run --rm cli python -c "from cli import __version__; print(__version__)"
   ```

## Notes

- All commands are stubs at this point
- Focus on structure and framework
- Actual implementation comes in later steps
- Ensure proper error handling

## Next Step
Proceed to Step 5: OLLAMA Integration
