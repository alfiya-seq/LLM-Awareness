import streamlit as st
import requests
import uuid
from db import add_message, get_messages, clear_messages

st.set_page_config(page_title="Local LLM Chat", layout="wide")
st.title(" Local Chat with tinyLLama (Ollama + FastAPI + SQLite)")

if "ui_messages" not in st.session_state:              # For adding check for clear chat button
    st.session_state.ui_messages = []


# Create/load session
import os

# Session ID logic
SESSION_FILE = "session_id.txt"                   # This session ID is how you fetch/save chats from DB per user.

if "session_id" not in st.session_state:           # st.session_state => streamlit built in memory, that keeps data while the app is open.
    if os.path.exists(SESSION_FILE):                # if session file has id,  store that in memory
        with open(SESSION_FILE, "r") as f:
            st.session_state.session_id = f.read()
    else:
        new_id = str(uuid.uuid4())                  # else create a new id using uuid and update in memory and write in session file (new user)
        st.session_state.session_id = new_id
        with open(SESSION_FILE, "w") as f:
            f.write(new_id)

# Add Model Selector
model = st.selectbox("Choose your model:", ["mistral", "tinyllama"])
st.session_state.model = model  # store in state if needed later

           
# Display previous messages
messages = get_messages(st.session_state.session_id)            # st.session_state = {'session_id': '4c15d117-088e-4427-8b08-7b656d7a9fd6'}
for msg in messages:
    with st.chat_message(msg.role):                           # Display a message bubble based on role .Streamlit’s special chat_message() context. It tells Streamlit: “Start a new chat bubble from the perspective of either a user or assistant.”
        st.markdown(msg.content)                           #This displays the actual message text inside the bubble st.markdown() is a Streamlit function that lets you use Markdown formatting (like bold, italics, code blocks).

# Input box
if prompt := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    add_message(st.session_state.session_id, "user", prompt)
    st.session_state.ui_messages.append(prompt)

    # Get response from FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = requests.post("http://localhost:8000/chat", json={"prompt": prompt,"model": model})
            response = res.json()["response"]
            st.markdown(response)
    add_message(st.session_state.session_id, "assistant", response)
    st.session_state.ui_messages.append(res)

# Clear history
if st.session_state.ui_messages or messages:
    if st.button(" Clear Chat"):
        clear_messages(st.session_state.session_id)   #clear db
        st.session_state.ui_messages = []           # Clear UI memory
        st.rerun()
