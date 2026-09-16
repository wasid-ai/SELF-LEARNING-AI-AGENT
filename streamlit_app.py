import os
import re

import streamlit as st
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI


# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("OPENROUTER_API_KEY nahi mila. .env file check karo.")
    st.stop()


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Self Learning AI Agent",
    page_icon="🤖",
    layout="centered"
)


# =========================
# MEM0 CONFIGURATION
# =========================

memory_config = {
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
}


# =========================
# LOAD SERVICES ONCE
# =========================

@st.cache_resource
def load_services():

    memory = Memory.from_config(memory_config)

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    return memory, client


memory, client = load_services()


# =========================
# USER ID
# =========================

st.sidebar.title("👤 User")

user_id_input = st.sidebar.text_input(
    "User ID",
    value="wasid",
    help="Each User ID has separate long-term memories."
)


# Clean User ID
user_id = re.sub(r"[^a-zA-Z0-9_-]", "_", user_id_input.strip())

if not user_id:
    user_id = "wasid"


st.sidebar.info(
    f"Current User ID:\n\n**{user_id}**"
)


# =========================
# MAIN UI
# =========================

st.title("🤖 Self Learning AI Agent")

st.write(
    "A general-purpose AI chatbot enhanced with "
    "long-term memory using Mem0 and Qdrant."
)


st.caption(
    "Memory is isolated using User ID."
)


# =========================
# CHAT HISTORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# CHAT INPUT
# =========================

user_message = st.chat_input(
    "Type your message..."
)


if user_message:

    # -------------------------
    # Display user message
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)


    # -------------------------
    # Search long-term memory
    # -------------------------

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

        memories = []

        st.warning(
            f"Memory search failed: {e}"
        )


    # -------------------------
    # Prepare memory context
    # -------------------------

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


    # -------------------------
    # AI SYSTEM PROMPT
    # -------------------------

    system_prompt = """
You are a helpful general-purpose AI assistant.

You have access to relevant long-term memories about the current user.

Use those memories when they are relevant to the user's question.

Do not mention the memory system unless it is useful to explain your answer.

If a memory is irrelevant, ignore it.

Give clear and helpful answers.
"""


    if memory_context:

        system_prompt += memory_context


    # -------------------------
    # Prepare messages
    # -------------------------

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


    # Keep recent conversation history

    messages.extend(
        st.session_state.messages[-10:]
    )


    # -------------------------
    # Generate AI response
    # -------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=messages
                )

                answer = response.choices[0].message.content

            except Exception as e:

                answer = (
                    "AI response generate karne me error aaya:\n\n"
                    f"{e}"
                )

            st.markdown(answer)


    # -------------------------
    # Save assistant response
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # -------------------------
    # Save user message to memory
    # -------------------------

    try:

        memory.add(
            user_message,
            user_id=user_id
        )

    except Exception as e:

        st.warning(
            f"Memory save failed: {e}"
        )


# =========================
# SIDEBAR INFORMATION
# =========================

st.sidebar.divider()

st.sidebar.subheader("🧠 Long-Term Memory")

st.sidebar.write(
    "Each User ID gets its own memory space."
)

st.sidebar.write(
    "Example:"
)

st.sidebar.code(
    "wasid\nuser_001\nuser_002"
)

st.sidebar.divider()

st.sidebar.caption(
    "Built with Python + Streamlit + Mem0 + "
    "Qdrant + OpenRouter"
)