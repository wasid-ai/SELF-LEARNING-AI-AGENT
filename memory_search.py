from mem0 import Memory

memory = Memory()

query = "What is my name and what am I learning?"

results = memory.search(
    query,
    filters={"user_id": "wasid"}
)

print("Memory search results:")
print(results)