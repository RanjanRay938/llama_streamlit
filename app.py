import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# LOAD ENV 
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# UI 
st.set_page_config(page_title="LLaMA Chatbot", page_icon="")
st.title("Ranjan  Chatbot")
st.caption("Powered by Groq (LLaMA-3)")

#  SESSION STATE -
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

    #  DISPLAY CHAT 
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    #  USER INPUT
prompt = st.chat_input("Ask something...")

if prompt:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response)

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
