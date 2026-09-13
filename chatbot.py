import os

from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY nahi mila. .env file check karo."
    )


memory_config = {
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


print("\nLong-Term Memory AI Agent")
print("Type 'exit' to stop.\n")


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    memories = memory.search(
        user_input,
        filters={"user_id": "wasid"}
    )

    print("\nRelevant memories:")

    for item in memories.get("results", []):
        print("-", item["memory"])

    context = "\n".join(
        item["memory"]
        for item in memories.get("results", [])
    )

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant with long-term memory. "
                    "Use the following memories when answering:\n"
                    + context
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    answer = response.choices[0].message.content

    print("\nAI:", answer)

    memory.add(
        [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": answer}
        ],
        user_id="wasid"
    )

    print("Memory updated successfully.\n")