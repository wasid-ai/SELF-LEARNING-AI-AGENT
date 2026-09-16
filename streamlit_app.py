import os

import streamlit as st
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("OPENROUTER_API_KEY nahi mila. .env file check karo.")
    st.stop()


st.set_page_config(
    page_title="Self-Learning AI Agent",
    page_icon="🤖",
    layout="centered"
)


@st.cache_resource
def initialize_agent():

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

    memory = Memory.from_config(memory_config)

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    return memory, client


memory, client = initialize_agent()


st.title("🤖 SELF-LEARNING AI AGENT")
st.caption("AI Chatbot with Long-Term Memory")

st.divider()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type your message...")


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)


    memories = memory.search(
        user_input,
        filters={"user_id": "wasid"}
    )

    context = "\n".join(
        item["memory"]
        for item in memories.get("results", [])
    )


    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI assistant with long-term memory. "
                            "Use relevant memories when answering. "
                            "If memories are not relevant, answer normally.\n\n"
                            "Relevant memories:\n"
                            + context
                        )
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            answer = response.choices[0].message.content

            st.markdown(answer)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    memory.add(
        [
            {
                "role": "user",
                "content": user_input
            },
            {
                "role": "assistant",
                "content": answer
            }
        ],
        user_id="wasid"
    )