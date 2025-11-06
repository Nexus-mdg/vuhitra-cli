# Step 6: Elasticsearch Heuristics & Cache

## Objective
Implement Elasticsearch integration for prompt heuristics storage and similarity-based caching.

## Context
Elasticsearch will store two types of data:
1. **Heuristics**: Behavior patterns of prompts (always enabled)
2. **Prompt Cache**: Similar prompts and their responses (disabled by default)

## Requirements

### Index Schemas

#### Heuristics Index
```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "signature": {"type": "keyword"},
      "prompt": {"type": "text"},
      "prompt_hash": {"type": "keyword"},
      "model": {"type": "keyword"},
      "behavior": {
        "type": "object",
        "properties": {
          "success": {"type": "boolean"},
          "tokens_used": {"type": "integer"},
          "response_time_ms": {"type": "float"},
          "error": {"type": "text"}
        }
      },
      "metadata": {
        "type": "object",
        "properties": {
          "intent": {"type": "keyword"},
          "entities": {"type": "keyword"},
          "sentiment": {"type": "float"}
        }
      },
      "timestamp": {"type": "date"}
    }
  }
}
```

#### Prompt Cache Index
```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "signature": {"type": "keyword"},
      "prompt": {"type": "text"},
      "prompt_normalized": {"type": "text"},
      "response": {"type": "text"},
      "model": {"type": "keyword"},
      "timestamp": {"type": "date"},
      "hit_count": {"type": "integer"}
    }
  }
}
```

### Implementation Files

**cli/src/cli/services/elastic_client.py**
**cli/src/cli/utils/prompt_signature.py**

## Key Implementation Points

- Create/manage indices
- Store heuristics after each AI interaction
- Cache lookup with similarity search
- Signature generation (NLP-based)
- TTL and cleanup strategies

## Validation
- Create indices successfully
- Store and retrieve heuristics
- Cache lookup works
- Similarity search functional

## Next Step
Proceed to Step 7: Redis Vector Store & Data Cache
