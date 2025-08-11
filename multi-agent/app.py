# app.py

import streamlit as st
from agents.code_writer import generate_code
from agents.test_generator import generate_tests
from agents.flow_runner import run_code_writer_and_test

st.set_page_config(page_title="Multi-Agent Coder", layout="wide")

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
st.sidebar.title("🛠️ Settings")
model = st.sidebar.selectbox("Select Model", ["mistral"])
language = st.sidebar.selectbox("Select Language", ["Python", "JavaScript", "C++", "Java", "Go"])
if st.sidebar.button("🧹 Clear Conversation"):
    st.session_state.messages = []

# --- Main Chat Interface ---
st.title("Multi-Agent Coder")
chat_container = st.container()

# Show full message history
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        elif msg["role"] == "assistant":
            content = msg.get("content", "")
            if content:
                st.chat_message("assistant").markdown(content)

# Chat input
user_input = st.chat_input("Enter your coding task here...")

if user_input and user_input.strip() != "":
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Run agents
        with st.spinner("🚀 Running agents...Generating code & Tests"):
            code, tests = run_code_writer_and_test(user_input, language, model)

        print("DEBUG - code:", repr(code))
        print("DEBUG - tests:", repr(tests))

        # Build assistant reply
        full_response = full_response = f"### 🧑‍💻 Generated Code:\n{code.strip()}\n\n" \
                f"### 🧪 Test Cases (pytest):\n{tests.strip()}"
        print("DEBUG - full_response:", repr(full_response))
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# 🧼 Render all messages exactly once
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        elif msg["role"] == "assistant":
            st.chat_message("assistant").markdown(msg["content"])
