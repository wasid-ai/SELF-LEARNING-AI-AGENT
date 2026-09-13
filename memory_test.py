from mem0 import Memory

memory = Memory()

messages = [
    {
        "role": "user",
        "content": "My name is Wasid and I am learning AI and Machine Learning."
    }
]

result = memory.add(messages, user_id="wasid")

print("Memory added successfully!")
print(result)