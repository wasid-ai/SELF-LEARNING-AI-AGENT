# AI Agent with Long-Term Memory

An AI chatbot built with Python, Mem0, Qdrant, and OpenRouter. The project can remember user information, retrieve relevant memories, and update preferences during future conversations.

## Features

- Stores user information in long-term memory
- Retrieves relevant memories using Mem0
- Updates old preferences with new information
- Uses Qdrant for local vector storage
- Uses OpenRouter for AI responses
- Loads the API key securely from a `.env` file
- Interactive command-line chatbot
- Local memory storage for continued conversations

## Technologies Used

- Python
- Mem0
- Qdrant
- OpenAI Python SDK
- OpenRouter
- python-dotenv

## Project Structure

```text
ai-agent-long-term-memory/
│
├── chatbot.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
├── qdrant_data/
└── .venv/
## How It Works

1. The user enters a message.
2. The application searches for relevant memories.
3. Mem0 retrieves previously stored information.
4. The retrieved memories are provided to the AI model.
5. The AI generates a response.
6. The conversation is saved in long-term memory.
7. New information can update previously stored preferences.

## Installation

### 1. Clone the Repository

    git clone YOUR_GITHUB_REPOSITORY_URL
    cd ai-agent-long-term-memory

### 2. Create a Virtual Environment

    python -m venv .venv

### 3. Activate the Virtual Environment on Windows

    .venv\Scripts\activate

### 4. Install Dependencies

    pip install -r requirements.txt

## Environment Variables

Create a `.env` file in the project folder:

    OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY

Replace `YOUR_OPENROUTER_API_KEY` with your own OpenRouter API key.

**Important:** Never publish your real API key on GitHub.

## Run the Project

Run the chatbot using:

    python chatbot.py

After starting the application, enter messages at the `You:` prompt.

To stop the chatbot, type:

    exit

## Example

    Long-Term Memory AI Agent
    Type 'exit' to stop.

    You: My name is Wasid.

    AI: Nice to meet you, Wasid!

    You: What is my name?

    AI: Your name is Wasid.

## Memory Update Example

    You: My favorite food is pasta.

    You: I don't like pasta anymore. My favorite food is biryani.

    You: What is my favorite food?

    AI: Your favorite food is biryani.

## Important Notes

- The `.env` file must not be uploaded to GitHub.
- The `qdrant_data/` folder contains local memory data.
- The `.venv/` folder is excluded from version control.
- The `.gitignore` file prevents private and unnecessary files from being uploaded.
- An OpenRouter API key is required to generate AI responses.
- Qdrant is used for local memory storage.
- The chatbot currently runs through the command line.

## Future Improvements

- Add a graphical user interface
- Build a Streamlit web application
- Add support for multiple users
- Add memory management commands
- Add conversation history display
- Improve error handling
- Add automated tests
- Deploy the chatbot online
- Add voice input and output

## Author

Wasid Khan