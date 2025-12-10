import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit page settings
st.set_page_config(page_title="Week 10 ChatGPT App", page_icon="💬")
st.title("💬 Week 10 - Simple ChatGPT App")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant for the Week 10 lab."
        }
    ]

# Display previous chat messages (skip system role)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add user message to session history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    reply = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages
    ).choices[0].message.content

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
