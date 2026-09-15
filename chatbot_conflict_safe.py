import os
import json
import re

from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI


# --------------------------------------------------
# 1. Environment setup
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY nahi mila. .env file check karo."
    )


# --------------------------------------------------
# 2. Mem0 + Qdrant setup
# --------------------------------------------------

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


# --------------------------------------------------
# 3. OpenRouter setup
# --------------------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "openai/gpt-4o-mini"
USER_ID = "wasid"


# --------------------------------------------------
# 4. Explicit preference detection
# --------------------------------------------------

def detect_food_preference(user_input):
    """
    Sirf clear food-preference statements detect karta hai.
    Random sentences par memory delete nahi karega.
    """

    text = user_input.lower().strip()

    # Explicit rejection statements
    rejection_patterns = [
        r"i do not like ([a-zA-Z ]+)",
        r"i don't like ([a-zA-Z ]+)",
        r"i no longer like ([a-zA-Z ]+)",
        r"i dislike ([a-zA-Z ]+)",
    ]

    for pattern in rejection_patterns:
        match = re.search(pattern, text)

        if match:
            food = match.group(1).strip()
            food = re.sub(
                r"\banymore\b|\bnow\b|\bplease\b",
                "",
                food
            ).strip()

            return {
                "type": "rejection",
                "food": food
            }

    # Explicit current preference statements
    preference_patterns = [
        r"my favorite food is ([a-zA-Z ]+)",
        r"my favourite food is ([a-zA-Z ]+)",
        r"i like ([a-zA-Z ]+)",
        r"i love ([a-zA-Z ]+)",
    ]

    for pattern in preference_patterns:
        match = re.search(pattern, text)

        if match:
            food = match.group(1).strip()
            food = re.sub(
                r"\banymore\b|\bnow\b|\bplease\b",
                "",
                food
            ).strip()

            return {
                "type": "preference",
                "food": food
            }

    return None


# --------------------------------------------------
# 5. Retrieve all user memories
# --------------------------------------------------

def get_all_user_memories():
    """
    Mem0 search relevant memories return karta hai.
    Food-related conflict ke liye broad search use kiya gaya hai.
    """

    result = memory.search(
        "user personal preferences favorite food likes dislikes",
        filters={"user_id": USER_ID},
        limit=20
    )

    return result.get("results", [])


# --------------------------------------------------
# 6. Display memories
# --------------------------------------------------

def print_memories(title, memories):
    print(f"\n{title}")

    if not memories:
        print("- No memories found.")
        return

    for item in memories:
        print("-", item.get("memory", ""))


# --------------------------------------------------
# 7. Main chatbot
# --------------------------------------------------

print("\nSafe Conflict-Resolution AI Agent")
print("Type 'memories' to view memories.")
print("Type 'exit' to stop.\n")


while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input:
        print("Please enter a message.\n")
        continue

    if user_input.lower() == "memories":
        all_memories = get_all_user_memories()
        print_memories("Stored memories:", all_memories)
        print()
        continue

    # --------------------------------------------------
    # Retrieve relevant memories for chatbot response
    # --------------------------------------------------

    search_result = memory.search(
        user_input,
        filters={"user_id": USER_ID},
        limit=5
    )

    relevant_memories = search_result.get("results", [])

    print_memories(
        "Relevant memories:",
        relevant_memories
    )

    context = "\n".join(
        item.get("memory", "")
        for item in relevant_memories
    )

    # --------------------------------------------------
    # Generate AI response
    # --------------------------------------------------

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant with long-term memory. "
                    "Use memories only when relevant. "
                    "Never invent personal information.\n\n"
                    f"Memories:\n{context}"
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

    # --------------------------------------------------
    # Safe explicit preference handling
    # --------------------------------------------------

    preference_event = detect_food_preference(user_input)

    if preference_event:
        print("\nDetected preference event:")
        print(
            f"- Type: {preference_event['type']}\n"
            f"- Food: {preference_event['food']}"
        )

        if preference_event["type"] == "preference":
            new_food = preference_event["food"]

            safe_memory = (
                f"User's current favorite food is {new_food}."
            )

            memory.add(
                safe_memory,
                user_id=USER_ID
            )

            print(
                "\nSafe action: Current food preference saved."
            )

        elif preference_event["type"] == "rejection":
            rejected_food = preference_event["food"]

            rejection_memory = (
                f"User no longer likes {rejected_food}."
            )

            memory.add(
                rejection_memory,
                user_id=USER_ID
            )

            print(
                "\nSafe action: Rejected food preference recorded."
            )

    else:
        # Normal conversation Mem0 ko di jayegi
        memory.add(
            [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": answer}
            ],
            user_id=USER_ID
        )

        print("\nNormal conversation saved.")

    print()