# SELF-LEARNING-AI-AGENT

An AI chatbot with long-term memory that can store, retrieve, and update user information using Mem0, Qdrant, and an OpenRouter-powered AI model.

## Features

* Long-term user memory
* Semantic memory retrieval
* Local vector storage using Qdrant
* AI responses using OpenRouter
* Advanced memory processing
* Preference conflict detection
* Safe preference updates and rejection handling
* Manual memory viewing and deletion
* Command-line interface

## How It Works

1. The user enters a message.
2. The agent searches stored memories.
3. Relevant memories are retrieved from Mem0 and Qdrant.
4. Retrieved context is provided to the AI model.
5. The AI generates a response.
6. New user information can be stored as long-term memory.
7. Updated preferences can be detected and handled safely.

## Technologies

* Python
* Mem0
* Qdrant
* OpenRouter
* OpenAI-compatible LLM API
* python-dotenv

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
├── .env              # Local only - not committed
├── .venv/            # Local virtual environment
└── qdrant_data/      # Local Qdrant storage
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/wasid-ai/SELF-LEARNING-AI-AGENT.git
cd SELF-LEARNING-AI-AGENT
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment on Windows

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project folder:

```env
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
```

Replace `YOUR_OPENROUTER_API_KEY` with your own OpenRouter API key.

**Never upload your real API key to GitHub.**

## Run the Basic Chatbot

```bash
python chatbot.py
```

## Run the Advanced Memory Agent

```bash
python chatbot_advanced.py
```

## Run the Conflict-Safe Agent

```bash
python chatbot_conflict_safe.py
```

This version detects explicit preference changes and rejection events before recording them as memory.

## Memory Manager

To view or manually delete stored memories:

```bash
python memory_manager.py
```

The memory manager provides options to:

1. Show stored memories
2. Delete a selected memory
3. Exit

## Example

```text
Long-Term Memory AI Agent
Type 'exit' to stop.

You: My name is Wasid.

AI: Nice to meet you, Wasid!

You: What is my name?

AI: Your name is Wasid.
```

## Memory Update Example

```text
You: My favorite food is pasta.

You: I no longer like pasta. My favorite food is biryani.

You: What is my favorite food?

AI: Your favorite food is biryani.
```

## Important Notes

* An OpenRouter API key is required.
* The `.env` file must remain private.
* Qdrant provides local vector storage.
* Local Qdrant data is excluded from version control.
* The project currently runs through the command line.
* Some optional Mem0 NLP and keyword-search components may require additional packages.

## Future Improvements

* Streamlit web interface
* Multi-user memory isolation
* Improved memory ranking and retrieval
* Automated unit and integration tests
* Complete conversation-history management
* Document and PDF memory
* Voice input and output
* External tool integration
* Authentication and privacy controls
* Monitoring and evaluation
* Cloud deployment

## Author

**Wasid Khan**

GitHub: https://github.com/wasid-ai

## Demo

The AI agent can retrieve previously stored memories and use them to answer future questions.

```text
You: What is my name?

Relevant memories:
- User's name is Wasid.

AI: Your name is Wasid.
```
