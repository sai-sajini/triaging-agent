import streamlit as st
from chat_manager import ChatManager
from llm import call_github_llm

# Initialize session state for chat manager
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()
    st.session_state.chat_manager.new_chat()

chat_manager = st.session_state.chat_manager

# Sidebar: Chat list and New Chat button
st.sidebar.title("Chats")
if st.sidebar.button("New Chat"):
    chat_manager.new_chat()

chat_ids = chat_manager.get_all_chats()
chat_titles = [chat_manager.get_chat_title(cid) for cid in chat_ids]
selected_chat = st.sidebar.radio("Select a chat:", chat_ids, format_func=lambda cid: chat_manager.get_chat_title(cid))
chat_manager.set_active_chat(selected_chat)

st.sidebar.markdown("---")
st.sidebar.caption("Triaging Agent Chatbot")

# Main chat window
st.title("🤖 Triaging Agent Chatbot")
st.markdown("<style>div.stChatMessage {margin-bottom: 1em;} .user-msg {background:#f0f4f8;padding:8px;border-radius:8px;} .assistant-msg {background:#e6f7e6;padding:8px;border-radius:8px;} .stTextInput>div>input {border-radius:8px;}</style>", unsafe_allow_html=True)

chat_history = chat_manager.get_chat_history()
for msg in chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="stChatMessage user-msg"><b>User:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="stChatMessage assistant-msg"><b>Assistant:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# Input box
user_input = st.text_input("Type your message...", key="input", on_change=None)
if user_input:
    chat_manager.add_message("user", user_input)
    assistant_response = call_github_llm(user_input)
    chat_manager.add_message("assistant", assistant_response)
    st.experimental_rerun()
