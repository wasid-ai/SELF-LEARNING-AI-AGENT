import os

from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY nahi mila.")


memory_config = {
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

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


def test_memory_save_and_retrieve():
    test_text = "My test project name is Self Learning AI Agent."

    memory.add(
        test_text,
        user_id="automated_test_user"
    )

    results = memory.search(
        "What is my test project name?",
        filters={"user_id": "automated_test_user"}
    )

    memories = results.get("results", [])

    assert len(memories) > 0, "Memory retrieval failed."

    print("PASS: Memory save and retrieval")


def test_ai_response():
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Say exactly: AI test successful."
            }
        ]
    )

    answer = response.choices[0].message.content

    assert answer, "AI response is empty."

    print("PASS: AI response")


if __name__ == "__main__":
    print("\nRunning automated tests...\n")

    test_memory_save_and_retrieve()
    test_ai_response()

    print("\nALL TESTS PASSED! ✅")