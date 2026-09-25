import os
import re

import streamlit as st
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
from ddgs import DDGS


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Self Learning AI Agent",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

api_key = None

# Streamlit Cloud Secrets
try:
    api_key = st.secrets.get("OPENROUTER_API_KEY")
except Exception:
    api_key = None

# Local .env fallback
if not api_key:
    api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("❌ OPENROUTER_API_KEY nahi mila.")
    st.info(
        "Streamlit Cloud → Settings → Secrets mein "
        "OPENROUTER_API_KEY add karo."
    )
    st.stop()

api_key = str(api_key).strip()

if not api_key:
    st.error("❌ OPENROUTER_API_KEY empty hai.")
    st.stop()


# =========================================================
# MEM0 CONFIGURATION
# =========================================================

memory_config = {
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": api_key,
            "openai_base_url": "https://openrouter.ai/api/v1",
            "model": "openai/gpt-4o-mini"
        }
    },

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



# =========================================================
# LOAD SERVICES
# =========================================================

@st.cache_resource
def load_services():

    memory = Memory.from_config(memory_config)

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    return memory, client


try:

    memory, client = load_services()

except Exception as e:

    st.error("❌ Services load nahi ho paayi.")

    st.code(str(e))

    st.stop()


# =========================================================
# WEB SEARCH
# =========================================================

def web_search(query, max_results=5):

    try:

        results = DDGS().text(
            query,
            max_results=max_results
        )

        return list(results)

    except Exception as e:

        st.warning(
            f"Web search failed: {e}"
        )

        return []


# =========================================================
# SEARCH DECISION
# =========================================================

def needs_web_search(query):

    query_lower = query.lower()

    current_keywords = [
        "latest",
        "today",
        "current",
        "now",
        "recent",
        "news",
        "this week",
        "this month",
        "2026",
        "price",
        "prices",
        "weather",
        "score",
        "result",
        "results",
        "new",
        "recently",
        "bigg boss",
        "election",
        "stock",
        "market"
    ]

    for keyword in current_keywords:

        if keyword in query_lower:
            return True

    return False


# =========================================================
# USER ID
# =========================================================

st.sidebar.title("👤 User")

user_id_input = st.sidebar.text_input(
    "User ID",
    value="wasid",
    help="Each User ID has separate long-term memories."
)

user_id = re.sub(
    r"[^a-zA-Z0-9_-]",
    "_",
    user_id_input.strip()
)

if not user_id:

    user_id = "wasid"


st.sidebar.info(
    f"Current User ID:\n\n**{user_id}**"
)


# =========================================================
# MAIN UI
# =========================================================

st.title("🤖 Self Learning AI Agent")

st.write(
    "A general-purpose AI chatbot enhanced with "
    "long-term memory and free web search."
)

st.caption(
    "Mem0 + Qdrant + OpenRouter + Free Web Search"
)


# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_message = st.chat_input(
    "Ask anything..."
)


if user_message:

    # =====================================================
    # DISPLAY USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):

        st.markdown(user_message)


    # =====================================================
    # MEMORY SEARCH
    # =====================================================

    memories = []

    try:

        memory_results = memory.search(
            user_message,
            filters={
                "user_id": user_id
            }
        )

        memories = memory_results.get(
            "results",
            []
        )

    except Exception as e:

        st.warning(
            f"Memory search failed: {e}"
        )


    # =====================================================
    # MEMORY CONTEXT
    # =====================================================

    memory_context = ""

    if memories:

        memory_lines = []

        for item in memories[:5]:

            memory_text = item.get(
                "memory",
                ""
            )

            if memory_text:

                memory_lines.append(
                    f"- {memory_text}"
                )

        if memory_lines:

            memory_context = (
                "\n\nRelevant long-term memories:\n"
                + "\n".join(memory_lines)
            )


    # =====================================================
    # WEB SEARCH
    # =====================================================

    search_results = []

    if needs_web_search(user_message):

        with st.spinner(
            "🌐 Searching the web..."
        ):

            search_results = web_search(
                user_message,
                max_results=5
            )


    # =====================================================
    # WEB CONTEXT
    # =====================================================

    web_context = ""

    if search_results:

        web_lines = []

        for result in search_results:

            title = result.get(
                "title",
                ""
            )

            body = result.get(
                "body",
                ""
            )

            href = result.get(
                "href",
                ""
            )

            web_lines.append(
                f"Title: {title}\n"
                f"Information: {body}\n"
                f"Source: {href}"
            )

        web_context = (
            "\n\nCurrent web search results:\n\n"
            + "\n\n".join(web_lines)
        )


    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = """
You are a helpful general-purpose AI assistant.

You have access to:

1. Relevant long-term memories about the current user.
2. Current web search results when available.

Use long-term memories only when they are relevant.

When web search results are provided, use them for current
or recent information.

Do not invent current facts when reliable web information
is available.

If web search results are unavailable, clearly say that
current information could not be verified.

Give clear, useful and concise answers.

Do not expose private memory information unless it is
relevant to the current user.

When using web information, mention useful source links
when appropriate.
"""


    if memory_context:

        system_prompt += memory_context


    if web_context:

        system_prompt += web_context


    # =====================================================
    # AI MESSAGES
    # =====================================================

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(
        st.session_state.messages[-10:]
    )


    # =====================================================
    # AI RESPONSE
    # =====================================================

    answer = ""

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Thinking..."
        ):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=messages,
                    temperature=0.7
                )

                answer = (
                    response.choices[0]
                    .message
                    .content
                )

            except Exception as e:

                answer = (
                    "❌ AI response generate karne "
                    "me error aaya:\n\n"
                    f"{e}"
                )

            st.markdown(answer)


    # =====================================================
    # WEB SOURCES
    # =====================================================

    if search_results:

        st.markdown(
            "### 🌐 Web Sources"
        )

        for result in search_results:

            title = result.get(
                "title",
                "Source"
            )

            href = result.get(
                "href",
                ""
            )

            if href:

                st.markdown(
                    f"- [{title}]({href})"
                )


    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # =====================================================
    # SAVE USER MEMORY
    # =====================================================

    try:

        memory.add(
            user_message,
            user_id=user_id
        )

    except Exception as e:

        st.warning(
            f"Memory save failed: {e}"
        )


# =========================================================
# SIDEBAR INFORMATION
# =========================================================

st.sidebar.divider()

st.sidebar.subheader(
    "🧠 Long-Term Memory"
)

st.sidebar.write(
    "Each User ID has a separate memory space."
)

st.sidebar.subheader(
    "🌐 Web Search"
)

st.sidebar.write(
    "Current information is searched using "
    "a free web-search layer."
)

st.sidebar.divider()

st.sidebar.caption(
    "Built with Python + Streamlit + Mem0 + "
    "Qdrant + OpenRouter + DDGS"
)
