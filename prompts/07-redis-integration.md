# Step 7: Redis Vector Store & Data Cache

## Objective
Implement Redis integration for RAG vector storage and temporary DataFrame caching.

## Context
Redis >= 7.2 supports vector operations and will be used for:
1. Vector storage for RAG (document embeddings)
2. Temporary DataFrame caching for R/Python/PySpark
3. Session data storage

## Requirements

### Features to Implement
- Vector storage and retrieval
- DataFrame serialization and caching with TTL
- Session management
- Search functionality

### Implementation File
**cli/src/cli/services/redis_client.py**

## Key Components

```python
class RedisClient:
    def __init__(self, url: str):
        # Initialize Redis connection
        
    def store_vector(self, key: str, vector: np.ndarray, metadata: dict):
        # Store embedding vector with metadata
        
    def search_vectors(self, query_vector: np.ndarray, top_k: int = 5):
        # Similarity search
        
    def store_dataframe(self, key: str, df, ttl: int = 3600):
        # Cache DataFrame with expiration
        
    def get_dataframe(self, key: str):
        # Retrieve cached DataFrame
        
    def store_session(self, session_id: str, data: dict, ttl: int = 86400):
        # Store session data
```

## Validation
- Connect to Redis
- Store and retrieve vectors
- Cache DataFrames
- TTL works correctly

## Next Step
Proceed to Step 8: Sandbox Service & File Handling
