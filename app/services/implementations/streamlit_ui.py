import streamlit as st
from app.services.interfaces.ui_interface import UIService


class StreamlitUIService(UIService):
    def __init__(self):
        self.messages = []

    def initialize(self) -> None:
        st.title("RAG Chat Interface")
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display_message(self, message: str, role: str) -> None:
        with st.chat_message(role):
            st.write(message)
        st.session_state.messages.append({"role": role, "content": message})

    def get_user_input(self) -> str:
        return st.chat_input("Your question:")

    def show_build_button(self) -> bool:
        return st.button("Build RAG Database", key="build_button")
