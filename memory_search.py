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
            "path": "qdrant_data"
        }
    }
}

memory = Memory.from_config(memory_config)
