import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from .env
api_key = os.getenv("OPENAI_API_KEY")

# Safety check
if not api_key:
    st.error("❌ OPENAI_API_KEY not found in .env file.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Week 10 ChatGPT App", page_icon="💬")
st.title("💬 Week 10 - Simple ChatGPT App")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant for a student studying Artificial Intelligence."
        }
    ]

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    # OpenAI API call
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        ).choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        st.info("Please check your OpenAI API key in the .env file")
