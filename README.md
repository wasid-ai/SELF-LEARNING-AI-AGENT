# SELF-LEARNING-AI-AGENT

A general-purpose AI chatbot enhanced with long-term memory, semantic retrieval, web search, multi-user memory isolation, and AI-powered responses.

This project combines Mem0, Qdrant, OpenRouter, Streamlit, and DDGS to create an AI agent that can remember user information, retrieve relevant memories, search the web for recent information, and generate contextual responses.

---

## 🚀 Features

- 🤖 General-purpose AI chatbot
- 🧠 Long-term memory using Mem0
- 🔎 Semantic memory retrieval
- 🗄️ Local vector storage using Qdrant
- 🌐 Free web search using DDGS
- 👥 Multi-user memory isolation using User IDs
- 🖥️ Streamlit web interface
- 🔌 OpenRouter-powered AI model
- 🧪 Automated tests
- 🔄 Preference conflict detection
- 🛡️ Conflict-safe memory updates
- 🧰 Manual memory viewing and deletion
- 💻 Command-line chatbot support
- 🔐 Environment-variable based API-key configuration

---

## 🧠 How It Works

The system combines an LLM, long-term memory, vector search, and web search into a single AI-agent workflow.

                         USER
                           │
                           ▼
                    Streamlit UI
                           │
                           ▼
                 Question Processing
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Memory       Web Search    Normal Query
           Search        (Current)       │
              │            │             │
              ▼            ▼             │
         Mem0 + Qdrant     DDGS          │
              │            │             │
              └────────────┼─────────────┘
                           │
                           ▼
                      OpenRouter
                           │
                           ▼
                     AI Response
                           │
                           ▼
                 Memory Processing
                           │
                           ▼
                 Long-Term Storage

### 🔄 Complete Workflow

1. The user enters a question or message.
2. The Streamlit application receives the input.
3. The system identifies the current User ID.
4. The agent searches the user's long-term memory.
5. Mem0 retrieves relevant memories from the Qdrant vector database.
6. The system checks whether the query requires recent/current information.
7. If current information is required, DDGS performs a web search.
8. Retrieved memories and web results are combined with the user's question.
9. The combined context is sent to the OpenRouter-powered AI model.
10. The AI generates a contextual response.
11. Relevant user information can be stored as long-term memory.
12. The response is displayed in the Streamlit interface.
13. When web search is used, available web sources are also displayed.

---

## 🧠 Memory Flow

User Message
     │
     ▼
Memory Search
     │
     ▼
Mem0
     │
     ▼
Qdrant Vector Database
     │
     ▼
Relevant Memories
     │
     ▼
AI Model
     │
     ▼
Response
     │
     ▼
Memory Update

The memory system allows the agent to retrieve previously stored information instead of depending only on the current conversation.

### Example

User:
My name is Wasid.

Agent:
Nice to meet you, Wasid!

User:
What is my name?

Agent:
Your name is Wasid.

---

## 🌐 Web Search

The project includes a free web-search layer using DDGS.

The web-search system is designed for information that may change over time.

Examples include:

- Latest news
- Current events
- Recent updates
- Current prices
- Recent technology developments
- Sports results
- Other time-sensitive information

### Web Search Workflow

User Question
      │
      ▼
Question Processing
      │
      ▼
Current Information Required?
      │
     YES
      │
      ▼
DDGS Web Search
      │
      ▼
Search Results
      │
      ▼
OpenRouter AI
      │
      ▼
AI Response + Web Sources

### Example

User:
What are the latest Bigg Boss updates?

Agent:
Searching the web...

Agent:
Uses recent search results to generate the response.

Web Sources:
- Search Result 1
- Search Result 2
- Search Result 3

The web-search layer complements the LLM by providing externally retrieved information when recent information is required.

> Web search depends on external search availability, and search results should be verified when accuracy is important.

---

## 👥 Multi-User Memory Isolation

The Streamlit application supports separate memory spaces using a User ID.

### Example

User ID: wasid
User ID: user_001
User ID: user_002

Each User ID is passed to the memory system when searching and storing information.

                    User ID
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
        wasid       user_001     user_002
          │            │            │
          ▼            ▼            ▼
       Memory A     Memory B     Memory C

This provides application-level memory separation so that memories associated with one User ID are not intentionally retrieved for another User ID.

### Example

User ID: wasid

User:
My name is Wasid.

Agent:
Nice to meet you, Wasid!

Another User ID:

User ID: user_001

User:
What is my name?

Agent:
I don't have your name stored in memory yet.

> Note: This is application-level memory isolation, not production authentication. A production deployment would additionally require authentication, authorization, secure user management, and stronger privacy controls.

---

## 🖥️ Streamlit Web Interface

The project includes a browser-based interface built using Streamlit.

The interface provides:

- 💬 Chat interface
- 👤 User ID selection
- 🧠 Long-term memory
- 🌐 Web search
- 🤖 AI-generated responses
- 🔎 Relevant web sources
- 👥 Separate memory spaces for different users

### Run the Application

streamlit run streamlit_app.py

After starting Streamlit, open the local URL shown in the terminal.

---

## 🧪 Automated Tests

The project includes automated tests for the core AI-agent functionality.

### Memory Tests

- Saving a test memory
- Retrieving the stored memory

### AI Tests

- Sending a request to the OpenRouter model
- Verifying that an AI response is returned

### Run Tests

python test_agent.py

### Expected Result

Running automated tests...

PASS: Memory save and retrieval
PASS: AI response

ALL TESTS PASSED! ✅

---

## 🧩 Preference Conflict Handling

The project includes a conflict-safe memory workflow for handling changed user preferences.

### Example

User:
My favorite food is pasta.

User:
I no longer like pasta. My favorite food is biryani.

Agent:
Detects the preference change and processes the updated preference.

This helps prevent outdated preferences from being treated as the user's current preference.

---

## 🧰 Memory Manager

The project includes a memory-management utility that allows stored memories to be viewed and manually deleted.

Run:

python memory_manager.py

The memory manager provides options for:

1. Viewing stored memories
2. Selecting a memory
3. Deleting a selected memory
4. Exiting the tool

---

## 💻 Command-Line Support

In addition to the Streamlit interface, the project contains command-line versions of the AI agent.

### Basic Chatbot

python chatbot.py

### Advanced Memory Agent

python chatbot_advanced.py

### Conflict-Safe Agent

python chatbot_conflict_safe.py

---

## 🛠️ Technologies

### Programming Language

- Python

### AI / LLM

- OpenRouter
- OpenAI-compatible API

### Memory

- Mem0
- Semantic memory retrieval

### Vector Database

- Qdrant

### Web Search

- DDGS

### User Interface

- Streamlit

### Configuration

- python-dotenv

---

## 📁 Project Structure

SELF-LEARNING-AI-AGENT/
│
├── chatbot.py
├── chatbot_advanced.py
├── chatbot_conflict_safe.py
├── streamlit_app.py
├── test_agent.py
├── memory_manager.py
├── memory_test.py
├── memory_search.py
├── main.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
├── .env              # Local only - not committed
├── .venv/            # Local virtual environment
└── qdrant_data/      # Local Qdrant storage

---

## ⚙️ Installation

### 1. Clone the Repository

git clone https://github.com/wasid-ai/SELF-LEARNING-AI-AGENT.git
cd SELF-LEARNING-AI-AGENT

### 2. Create a Virtual Environment

python -m venv .venv

### 3. Activate the Virtual Environment on Windows

.venv\Scripts\activate

### 4. Install Dependencies

pip install -r requirements.txt

---

## 🔐 Environment Variables

Create a .env file in the project folder.

OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY

Replace YOUR_OPENROUTER_API_KEY with your own API key.

Never upload your real API key to GitHub.

---

## ▶️ Running the Project

### Basic Chatbot

python chatbot.py

### Advanced Memory Agent

python chatbot_advanced.py

### Conflict-Safe Agent

python chatbot_conflict_safe.py

### Streamlit AI Agent

streamlit run streamlit_app.py

### Automated Tests

python test_agent.py

### Memory Manager

python memory_manager.py

---

## 💬 Basic Chat Example

You:
My name is Wasid.

AI:
Nice to meet you, Wasid!

You:
What is my name?

AI:
Your name is Wasid.

---

## 🌐 Web Search Example

You:
What are the latest technology updates?

Agent:
Searching the web...

AI:
Provides a response using recent search results.

Web Sources:
- Search Result 1
- Search Result 2
- Search Result 3

---

## 🧠 Long-Term Memory Example

You:
My name is Wasid.

You:
What is my name?

AI:
Your name is Wasid.

The agent retrieves the relevant information from long-term memory.

---

## 🔄 Memory Update Example

You:
My favorite food is pasta.

You:
I no longer like pasta. My favorite food is biryani.

You:
What is my favorite food?

AI:
Your favorite food is biryani.

---

## 👥 Multi-User Example

User ID: wasid

You:
My name is Wasid.

AI:
Nice to meet you, Wasid!

A different User ID has a separate memory space.

User ID: user_001

You:
What is my name?

AI:
I don't have your name stored in memory yet.

---

## 🧪 Testing Status

The current project has been tested for:

- ✅ Memory saving
- ✅ Memory retrieval
- ✅ AI response generation
- ✅ Multi-user memory isolation
- ✅ Streamlit chatbot functionality
- ✅ Web search integration
- ✅ Qdrant local storage
- ✅ OpenRouter integration
- ✅ Automated test execution

---

## ⚠️ Important Notes

- An OpenRouter API key is required.
- The .env file must remain private.
- Never commit API keys to GitHub.
- Qdrant is configured for local vector storage.
- Local Qdrant data is excluded from version control.
- Web search depends on external search availability.
- Current web information may require source verification.
- Multi-user support currently provides application-level memory isolation.
- It is not a complete authentication or authorization system.
- Some optional Mem0 NLP and keyword-search components may require additional packages.

---

## 🔒 Security

The project uses environment variables for API-key configuration.

The following files and directories should remain local:

.env
.venv/
qdrant_data/

These are excluded from Git version control through .gitignore.

Never hard-code an API key directly into the source code.

---

## 🔮 Future Improvements

- 🔐 Production authentication
- 🛡️ Stronger privacy and access controls
- 🧠 Improved memory ranking
- 🎯 More advanced question routing
- 📄 Document and PDF memory
- 🎙️ Voice input and output
- 🔌 External tool integrations
- 📊 Monitoring and evaluation
- 🧪 Better automated test coverage
- 💬 Conversation summarization
- ☁️ Cloud deployment
- 👥 Multi-user database architecture
- 📈 Memory analytics dashboard
- 🚀 Production-ready AI-agent deployment

---

## 🎯 Project Goal

The goal of this project is to explore how an AI assistant can become more useful by combining:

                    AI AGENT
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
       LLM      Long-Term Memory   Web Search
        │              │              │
        │              ▼              │
        │           Qdrant            │
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                Contextual Response

The project demonstrates how a chatbot can move beyond a stateless question-and-answer system by combining:

- Large Language Models
- Long-term memory
- Semantic retrieval
- Web search
- Multi-user support
- AI-agent workflows

---

## 📈 Current Capabilities

The current implementation demonstrates:

                    SELF-LEARNING AI AGENT
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 Long-Term Memory        Web Search           AI Responses
        │                     │                     │
        ▼                     ▼                     ▼
   Mem0 + Qdrant            DDGS              OpenRouter
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                       Streamlit Interface
                              │
                              ▼
                    Multi-User Memory

---

## 📌 Project Status

The project currently includes:

- ✅ AI chatbot
- ✅ Long-term memory
- ✅ Semantic retrieval
- ✅ Mem0 integration
- ✅ Qdrant vector database
- ✅ OpenRouter integration
- ✅ Streamlit web interface
- ✅ Free web search
- ✅ Multi-user memory isolation
- ✅ Automated tests
- ✅ Preference conflict handling
- ✅ Memory management
- ✅ Command-line support
- ✅ GitHub version control

The project is actively being improved toward a more complete and production-oriented AI-agent architecture.

---

## 👨‍💻 Author

**Wasid Khan**

GitHub: `wasid-ai`

---

## ⭐ Project

**SELF-LEARNING-AI-AGENT**

An AI agent designed to combine:

LLM
+
Long-Term Memory
+
Semantic Retrieval
+
Web Search
+
Multi-User Support

with a simple Streamlit interface for interactive use.