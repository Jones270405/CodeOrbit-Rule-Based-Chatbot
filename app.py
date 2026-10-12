
"""Streamlit interface for the Rule-Based Chatbot with persistent history."""

import streamlit as st

from chatbot import get_response
from chat_storage import (
    init_db,
    create_conversation,
    list_conversations,
    get_messages,
    save_message,
    update_title,
    clear_messages,
)

st.set_page_config(
    page_title="Rule-Based Chatbot",
    page_icon="💬",
    layout="centered",
)

# Initialize the SQLite database.
init_db()

st.title("💬 Rule-Based Chatbot")
st.caption(
    "A Python chatbot that answers predefined questions using rules."
)

# Initialize the active conversation.
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = create_conversation()

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# Sidebar
with st.sidebar:
    st.header("About this project")
    st.write(
        "This chatbot uses keyword rules, regular expressions, and "
        "predefined responses. It does not generate answers like a "
        "large language model."
    )

    st.divider()

    st.subheader("Try asking")

    suggestions = [
        "What is Python?",
        "What is machine learning?",
        "What is 25 + 37?",
        "What day is it today?",
        "Which music is best for relaxation?",
        "help",
    ]

    for index, suggestion in enumerate(suggestions):
        if st.button(
            suggestion,
            key=f"suggestion_{index}",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = suggestion
            st.rerun()

    st.divider()

    # Start a new conversation.
    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.conversation_id = create_conversation()
        st.rerun()

    # List saved conversations.
    st.subheader("Conversation History")

    conversations = list_conversations()

    if not conversations:
        st.caption("Your conversations will appear here.")
    else:
        for conversation in conversations:
            title = conversation["title"]

            if title == "New conversation":
                title = "Untitled conversation"

            is_active = (
                conversation["id"]
                == st.session_state.conversation_id
            )

            button_label = f"● {title}" if is_active else title

            if st.button(
                button_label,
                key=f"history_{conversation['id']}",
                use_container_width=True,
            ):
                st.session_state.conversation_id = conversation["id"]
                st.session_state.pending_prompt = None
                st.rerun()

    st.divider()

    if st.button("Clear current conversation", use_container_width=True):
        clear_messages(st.session_state.conversation_id)
        st.session_state.pending_prompt = None
        st.rerun()


# Load and display the active conversation.
conversation_id = st.session_state.conversation_id
saved_messages = get_messages(conversation_id)

if not saved_messages:
    st.chat_message("assistant").markdown(
        "Hello! I'm a rule-based chatbot. Ask me a supported question, "
        "or type **help** to see examples."
    )
else:
    for message in saved_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Process user input from the chat box or a suggested prompt.
prompt = st.chat_input("Type a message…")

if st.session_state.pending_prompt is not None:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt:
    prompt = prompt.strip()

    if prompt:
        # Give an empty conversation a title based on its first message.
        if not get_messages(conversation_id):
            update_title(conversation_id, prompt)

        # Save and display the user's message.
        save_message(conversation_id, "user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate, display, and save the response.
        response = get_response(prompt)

        with st.chat_message("assistant"):
            st.markdown(response)

        save_message(conversation_id, "assistant", response)

        # Refresh the history sidebar and displayed messages.
        st.rerun()
