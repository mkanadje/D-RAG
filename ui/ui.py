import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
backend_host = os.getenv("BACKEND_HOST", "http://localhost")
backend_port = os.getenv("BACKEND_PORT", "8080")

st.title("RAG Chatbot UI")

if st.button("Build RAG"):
    response = requests.post(f"{backend_host}:{backend_port}/build")
    if response.status_code == 200:
        st.success("RAG database built successfully.")
    else:
        st.error("Failed to build RAG database. Please check the backend logs.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input("Your question:")

if user_input:
    rag_exists = (
        requests.get(f"{backend_host}:{backend_port}/rag_exists")
        .json()
        .get("exists", False)
    )
    if not rag_exists:
        st.error("RAG database not built yet. Please build it first.")
    else:
        st.chat_message("User").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = requests.post(
            f"{backend_host}:{backend_port}/chat", json={"message": user_input}
        )
        if response.status_code == 200:
            result = response.json().get("answer", "No answer found.")
            with st.chat_message("Bot"):
                st.markdown(result)
            st.session_state.messages.append({"role": "bot", "content": result})
        else:
            with st.chat_message("Bot"):
                st.write("Error: Could not get a response from the backend.")
