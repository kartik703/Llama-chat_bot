import streamlit as st
import requests

# Set the Ollama endpoint
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"

st.set_page_config(page_title="🦙 LLaMA 2 Chatbot", page_icon="🦙")
st.title("🦙 LLaMA 2 Chatbot (Local, Free & Private)")

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send prompt to Ollama
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    OLLAMA_API,
                    json={
                        "model": MODEL_NAME,
                        "prompt": user_input,
                        "stream": False
                    }
                )
                output = response.json()["response"].strip()
            except Exception as e:
                output = f"❌ Error: {e}"

            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
