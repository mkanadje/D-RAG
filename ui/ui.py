import streamlit as st
import requests

st.title("RAG Chatbot UI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Your question:")

if user_input:
    st.chat_message("User").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = requests.post("http://backend:8000/chat", json={"message": user_input})
    if response.status_code == 200:
        result = response.json().get("answer", "No answer found.")
        with st.chat_message("Bot"):
            st.markdown(result)
        st.session_state.messages.append({"role": "bot", "content": result})
    else:
        with st.chat_message("Bot"):
            st.write("Error: Could not get a response from the backend.")
