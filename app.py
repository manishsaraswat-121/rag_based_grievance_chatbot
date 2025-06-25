import streamlit as st
from chatbot.chat_handler import get_bot_response
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit page setup
st.set_page_config(page_title="Grievance Assistant Bot", page_icon="🤖")
st.title("🤖 Grievance Assistant Bot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_state" not in st.session_state:
    st.session_state.chat_state = {}

# Reset button to clear the chat
if st.button("🔄 Reset Chat"):
    st.session_state.messages = []
    st.session_state.chat_state = {}
    st.rerun()

# Display chat history
for msg in st.session_state.messages:
    role, content = msg["role"], msg["content"]
    with st.chat_message(role):
        st.markdown(content)

# Chat input from user
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Get bot response
        bot_response = get_bot_response(user_input, st.session_state.chat_state)
    except Exception as e:
        bot_response = f"❌ Error: {e}"

    # Display bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(f"```\n{bot_response}\n```")
