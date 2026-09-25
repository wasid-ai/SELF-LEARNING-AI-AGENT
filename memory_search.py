from qdrant_client import QdrantClient
from mem0 import Memory

# Qdrant client in-memory mode mein initialize karein
qdrant_client = QdrantClient(location=":memory:")

memory_config = {
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": api_key,
            "openai_base_url": "https://openrouter.ai/api/v1",
            "model": "openai/gpt-4o-mini"
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": api_key,
            "openai_base_url": "https://openrouter.ai/api/v1",
            "model": "text-embedding-3-small"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "wasid_memories",
            "client": qdrant_client
        }
    }
}

memory = Memory.from_config(memory_config)

# Search operation
memory_results = memory.search(
    user_message,
    filters={"user_id": user_id}
)
