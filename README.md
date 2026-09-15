
# SELF-LEARNING-AI-AGENT

An AI chatbot with long-term memory built using Python, Mem0, Qdrant, and OpenRouter.

The project allows an AI agent to store user information, retrieve relevant memories during future conversations, and handle changing user preferences using memory and conflict-resolution logic.

## Features

- Long-term user memory
- Relevant memory retrieval using Mem0
- Local vector storage with Qdrant
- AI responses using OpenRouter
- Secure API-key loading through `.env`
- Interactive command-line chatbot
- Advanced memory processing
- Preference conflict detection
- Safe preference update and rejection handling
- Manual memory viewing and deletion
- Local persistent memory storage

## Technologies

- Python
- Mem0
- Qdrant
- OpenRouter
- OpenAI Python SDK
- python-dotenv

## Project Structure

```text
SELF-LEARNING-AI-AGENT/
│
├── chatbot.py
├── chatbot_advanced.py
├── chatbot_conflict_safe.py
├── memory_manager.py
├── memory_test.py
├── memory_search.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .env