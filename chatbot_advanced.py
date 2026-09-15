import os
import json

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
# 2. Mem0 + Qdrant configuration
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
# 3. OpenRouter client
# --------------------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


MODEL_NAME = "openai/gpt-4o-mini"
USER_ID = "wasid"


# --------------------------------------------------
# 4. Custom fact-extraction prompt
# --------------------------------------------------

FACT_EXTRACTION_PROMPT = """
You are a memory extraction system.

Read the conversation and identify only useful, stable,
user-specific facts that may help an AI assistant in future.

Focus on:
- Name
- Education
- Skills
- Career goals
- Favorite things
- Preferences
- Important project details
- Long-term habits
- Explicit changes in preferences

Do not save:
- Temporary greetings
- Small talk
- Repeated information
- Passwords
- API keys
- Sensitive private information
- Unsupported assumptions

Return only valid JSON in this format:

{
  "facts": [
    "fact 1",
    "fact 2"
  ]
}

If there are no useful facts, return:

{
  "facts": []
}
"""


# --------------------------------------------------
# 5. Custom memory-operation prompt
# --------------------------------------------------

MEMORY_UPDATE_PROMPT = """
You are a memory management system.

Compare the existing memories with the newly extracted facts.

For each new fact, decide one operation:

- ADD: Store a completely new fact.
- UPDATE: Replace or correct an existing fact.
- DELETE: Remove an outdated or explicitly rejected fact.
- NONE: Do nothing if the information is not useful.

Important rules:
- New explicit user statements have priority over old preferences.
- If the user changes a preference, update the old preference.
- Do not invent facts.
- Do not delete unrelated memories.
- Return only valid JSON.

Format:

{
  "operations": [
    {
      "operation": "ADD",
      "old_memory": "",
      "new_memory": "User likes pasta."
    }
  ]
}
"""


# --------------------------------------------------
# 6. Extract facts using the LLM
# --------------------------------------------------

def extract_facts(user_input, assistant_answer):
    conversation = (
        f"User: {user_input}\n"
        f"Assistant: {assistant_answer}"
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": FACT_EXTRACTION_PROMPT
            },
            {
                "role": "user",
                "content": conversation
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("\nWarning: Fact extraction returned invalid JSON.")
        return {"facts": []}


# --------------------------------------------------
# 7. Decide memory operations using the LLM
# --------------------------------------------------

def decide_memory_operations(existing_memories, extracted_facts):
    old_memories_text = "\n".join(
        f"- {item['memory']}"
        for item in existing_memories
    )

    new_facts_text = "\n".join(
        f"- {fact}"
        for fact in extracted_facts
    )

    prompt = (
        f"Existing memories:\n{old_memories_text}\n\n"
        f"New facts:\n{new_facts_text}"
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": MEMORY_UPDATE_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("\nWarning: Memory operation returned invalid JSON.")
        return {"operations": []}


# --------------------------------------------------
# 8. Main chatbot
# --------------------------------------------------

print("\nAdvanced Long-Term Memory AI Agent")
print("Custom fact extraction + memory operation analysis")
print("Type 'exit' to stop.\n")


while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input:
        print("Please enter a message.\n")
        continue

    # Retrieve relevant memories
    search_result = memory.search(
        user_input,
        filters={"user_id": USER_ID}
    )

    relevant_memories = search_result.get("results", [])

    print("\nRelevant memories:")

    if relevant_memories:
        for item in relevant_memories:
            print("-", item["memory"])
    else:
        print("- No relevant memories found.")

    context = "\n".join(
        item["memory"]
        for item in relevant_memories
    )

    # Generate assistant response
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant with long-term memory. "
                    "Use the following memories when answering. "
                    "Do not invent information.\n\n"
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

    # Extract new facts
    extracted_result = extract_facts(
        user_input,
        answer
    )

    extracted_facts = extracted_result.get("facts", [])

    print("\nExtracted facts:")

    if extracted_facts:
        for fact in extracted_facts:
            print("-", fact)
    else:
        print("- No useful facts found.")

    # Analyze memory operations
    operation_result = decide_memory_operations(
        relevant_memories,
        extracted_facts
    )

    print("\nSuggested memory operations:")

    operations = operation_result.get("operations", [])

    if operations:
        for operation in operations:
            print(
                f"- {operation.get('operation', 'NONE')}: "
                f"{operation.get('new_memory', '')}"
            )
    else:
        print("- No operations suggested.")

    # Let Mem0 perform its own memory management
    memory.add(
        [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": answer}
        ],
        user_id=USER_ID
    )

    print("\nMemory updated successfully.\n")