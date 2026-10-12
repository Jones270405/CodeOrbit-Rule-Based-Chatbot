"""Streamlit interface for the Rule-Based Chatbot."""
import streamlit as st
from chatbot import get_response

st.set_page_config(page_title="Rule-Based Chatbot", page_icon="💬", layout="centered")
st.title("💬 Rule-Based Chatbot")
st.caption("A Python chatbot that answers predefined questions using rules.")

with st.sidebar:
    st.header("About this project")
    st.write(
        "This chatbot uses keyword rules, regular expressions, and predefined "
        "responses. It does not generate answers like a large language model."
    )
    st.divider()
    st.subheader("Try asking")
    suggestions = [
        "What is Python?", "What is machine learning?", "What is 25 + 37?",
        "What day is it today?", "Which music is good for studying?", "help"
    ]
    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True):
            st.session_state.pending_prompt = suggestion

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm a rule-based chatbot. Ask me a supported question, or type **help** to see examples."
    }]
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if st.button("Clear conversation", type="secondary"):
    st.session_state.messages = [{
        "role": "assistant", "content": "Conversation cleared. What would you like to ask?"
    }]
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type a message…")
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": get_response(prompt)})
    st.rerun()
