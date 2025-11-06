# Step 5: OLLAMA Integration

## Objective
Implement OLLAMA model integration for AI inference with support for multiple models and streaming responses.

## Context
OLLAMA provides local AI model hosting. We need to create a robust client that can communicate with OLLAMA's API, handle multiple models (Llama, Qwen Coder), and support both streaming and non-streaming responses.

## Requirements

### OLLAMA Client Features
- Model listing and validation
- Prompt generation (streaming and non-streaming)
- Error handling and retries
- Timeout configuration
- Model switching
- Embedding generation (for RAG in later steps)

### Implementation File
`cli/src/cli/services/ollama_client.py`

## Implementation

```python
"""OLLAMA client for AI model interaction."""

import requests
import json
from typing import Generator, Optional, Dict, Any, List
from cli.logger import get_logger

logger = get_logger(__name__)


class OllamaError(Exception):
    """Base exception for OLLAMA errors."""
    pass


class OllamaConnectionError(OllamaError):
    """OLLAMA connection error."""
    pass


class OllamaModelError(OllamaError):
    """OLLAMA model error."""
    pass


class OllamaClient:
    """Client for OLLAMA API."""
    
    def __init__(self, base_url: str, model: str, timeout: int = 120):
        """Initialize OLLAMA client.
        
        Args:
            base_url: OLLAMA server URL (e.g., http://ollama:11434)
            model: Default model name
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        
        logger.info("Initialized OLLAMA client", extra={
            "base_url": self.base_url,
            "model": self.model
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request to OLLAMA API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments
            
        Returns:
            Response object
            
        Raises:
            OllamaConnectionError: If connection fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method,
                url,
                timeout=kwargs.pop('timeout', self.timeout),
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as e:
            logger.error("Failed to connect to OLLAMA", extra={"url": url})
            raise OllamaConnectionError(f"Cannot connect to OLLAMA at {url}") from e
        except requests.exceptions.Timeout as e:
            logger.error("OLLAMA request timeout", extra={"url": url})
            raise OllamaConnectionError(f"OLLAMA request timeout") from e
        except requests.exceptions.HTTPError as e:
            logger.error("OLLAMA HTTP error", extra={
                "url": url,
                "status": e.response.status_code
            })
            raise OllamaError(f"OLLAMA error: {e.response.text}") from e
    
    def health_check(self) -> bool:
        """Check if OLLAMA server is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            self._request('GET', '/api/tags')
            logger.info("OLLAMA health check passed")
            return True
        except Exception as e:
            logger.warning(f"OLLAMA health check failed: {str(e)}")
            return False
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List available models.
        
        Returns:
            List of model information dictionaries
        """
        response = self._request('GET', '/api/tags')
        models = response.json().get('models', [])
        
        logger.info(f"Listed {len(models)} models")
        return models
    
    def has_model(self, model_name: str) -> bool:
        """Check if model is available.
        
        Args:
            model_name: Name of the model
            
        Returns:
            True if model is available
        """
        models = self.list_models()
        model_names = [m['name'] for m in models]
        return model_name in model_names
    
    def pull_model(self, model_name: str) -> None:
        """Pull/download a model.
        
        Args:
            model_name: Name of the model to pull
        """
        logger.info(f"Pulling model: {model_name}")
        
        payload = {"name": model_name}
        response = self._request('POST', '/api/pull', json=payload, stream=True)
        
        # Stream pull progress
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'status' in data:
                    logger.debug(f"Pull status: {data['status']}")
        
        logger.info(f"Model pulled successfully: {model_name}")
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        stream: bool = False,
        options: Optional[Dict[str, Any]] = None
    ) -> str | Generator[str, None, None]:
        """Generate response from model.
        
        Args:
            prompt: Input prompt
            model: Model name (uses default if None)
            stream: Whether to stream response
            options: Additional generation options
            
        Returns:
            Complete response string or generator yielding chunks
        """
        model = model or self.model
        
        logger.info("Generating response", extra={
            "model": model,
            "stream": stream,
            "prompt_length": len(prompt)
        })
        
        # Ensure model is available
        if not self.has_model(model):
            logger.warning(f"Model not found, attempting to pull: {model}")
            self.pull_model(model)
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        if options:
            payload["options"] = options
        
        response = self._request('POST', '/api/generate', json=payload, stream=stream)
        
        if stream:
            return self._stream_response(response)
        else:
            result = response.json()
            return result.get('response', '')
    
    def _stream_response(self, response: requests.Response) -> Generator[str, None, None]:
        """Stream response chunks.
        
        Args:
            response: Streaming response object
            
        Yields:
            Text chunks
        """
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if 'response' in data:
                        yield data['response']
                    if data.get('done', False):
                        break
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in stream: {line}")
                    continue
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        stream: bool = False
    ) -> str | Generator[str, None, None]:
        """Chat with model using conversation format.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (uses default if None)
            stream: Whether to stream response
            
        Returns:
            Response string or generator
        """
        model = model or self.model
        
        logger.info("Chat request", extra={
            "model": model,
            "messages": len(messages)
        })
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        response = self._request('POST', '/api/chat', json=payload, stream=stream)
        
        if stream:
            return self._stream_chat_response(response)
        else:
            result = response.json()
            return result.get('message', {}).get('content', '')
    
    def _stream_chat_response(self, response: requests.Response) -> Generator[str, None, None]:
        """Stream chat response chunks.
        
        Args:
            response: Streaming response object
            
        Yields:
            Text chunks
        """
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if 'message' in data and 'content' in data['message']:
                        yield data['message']['content']
                    if data.get('done', False):
                        break
                except json.JSONDecodeError:
                    continue
    
    def embed(self, text: str, model: Optional[str] = None) -> List[float]:
        """Generate embeddings for text.
        
        Args:
            text: Input text
            model: Model name (uses default if None)
            
        Returns:
            List of embedding values
        """
        model = model or self.model
        
        logger.info("Generating embedding", extra={
            "model": model,
            "text_length": len(text)
        })
        
        payload = {
            "model": model,
            "prompt": text
        }
        
        response = self._request('POST', '/api/embeddings', json=payload)
        result = response.json()
        
        return result.get('embedding', [])
```

## Update chat.py Command

Update `cli/commands/chat.py` to use OLLAMA client:

```python
"""Chat command - interact with AI models."""

import click
from cli.services.ollama_client import OllamaClient, OllamaError


@click.command()
@click.argument('prompt', required=False)
@click.option('--stream', is_flag=True, help='Stream response')
@click.option('--model', help='Override default model')
@click.pass_context
def chat(ctx, prompt, stream, model):
    """Chat with AI model.
    
    Examples:
        vuhitra chat "What is Python?"
        vuhitra chat --stream "Explain machine learning"
        vuhitra chat --model qwen2.5-coder:7b "Write a Python function"
    """
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    if not prompt:
        prompt = click.prompt("Enter your prompt")
    
    # Initialize OLLAMA client
    ollama = OllamaClient(
        base_url=config.ollama_ip,
        model=model or config.model
    )
    
    # Check health
    if not ollama.health_check():
        click.echo("Error: Cannot connect to OLLAMA server", err=True)
        click.echo(f"URL: {config.ollama_ip}", err=True)
        return
    
    try:
        click.echo(f"Model: {model or config.model}")
        click.echo(f"Prompt: {prompt}\n")
        click.echo("Response:")
        click.echo("-" * 60)
        
        if stream:
            # Streaming response
            for chunk in ollama.generate(prompt, stream=True):
                click.echo(chunk, nl=False)
            click.echo()  # Final newline
        else:
            # Non-streaming response
            response = ollama.generate(prompt, stream=False)
            click.echo(response)
        
        click.echo("-" * 60)
        
    except OllamaError as e:
        logger.error(f"OLLAMA error: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
```

## Add Models Command

Create `cli/commands/models.py`:

```python
"""Model management commands."""

import click
from cli.services.ollama_client import OllamaClient


@click.group(name='models')
def models_group():
    """Manage OLLAMA models."""
    pass


@models_group.command(name='list')
@click.pass_context
def models_list(ctx):
    """List available models."""
    config = ctx.obj['config']
    
    ollama = OllamaClient(config.ollama_ip, config.model)
    
    try:
        models = ollama.list_models()
        
        if not models:
            click.echo("No models available")
            return
        
        click.echo(f"Available models ({len(models)}):\n")
        for model in models:
            click.echo(f"  - {model['name']}")
            if 'size' in model:
                size_gb = model['size'] / (1024**3)
                click.echo(f"    Size: {size_gb:.2f} GB")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@models_group.command(name='pull')
@click.argument('model_name')
@click.pass_context
def models_pull(ctx, model_name):
    """Pull/download a model."""
    config = ctx.obj['config']
    
    ollama = OllamaClient(config.ollama_ip, config.model)
    
    try:
        click.echo(f"Pulling model: {model_name}")
        click.echo("This may take a while...")
        
        ollama.pull_model(model_name)
        
        click.echo(f"✓ Model pulled successfully: {model_name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
```

Update `cli/main.py` to register models command:

```python
from cli.commands import chat, analyze, dev, cache, config_cmd, models

# ...

cli.add_command(models.models_group)
```

## Tasks

1. **Implement OLLAMA client**
   - Create ollama_client.py with all methods
   - Add error handling
   - Implement streaming support

2. **Update chat command**
   - Use OLLAMA client
   - Support streaming
   - Model override option

3. **Create models command**
   - List models
   - Pull models
   - Health check

4. **Add tests**
   - Unit tests for OLLAMA client
   - Mock OLLAMA API responses

## Expected Output

After completion:
- Working OLLAMA client
- Chat command with real AI responses
- Model management commands
- Streaming support

## Validation Steps

1. **Test connection** (requires OLLAMA running):
   ```bash
   docker-compose run --rm cli models list
   ```

2. **Test chat**:
   ```bash
   docker-compose run --rm cli chat "What is 2+2?"
   docker-compose run --rm cli chat --stream "Explain Python"
   ```

3. **Test model pull**:
   ```bash
   docker-compose run --rm cli models pull llama3:8b
   ```

## Notes

- Requires OLLAMA server running
- Configure OLLAMA_IP in .env
- Large models may take time to download
- Streaming provides better UX

## Next Step
Proceed to Step 6: Elasticsearch Heuristics & Cache
