"""Main entry point for the Knowledge Chatbot application."""

import logging
import os
import streamlit as st
from dotenv import load_dotenv

from services.ingestion import save_file_content
from services.rag import stream_answer

logger = logging.getLogger(__name__)

############## Preparations ##############
load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')
if not api_key or not api_key.strip():
    st.error("OPENAI_API_KEY is not set. Add it to your .env file (see .env.simple).")
    st.stop()


def render_answer():
    """ Finds the answer """
    question = st.session_state.user_question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    if st.session_state['last_processed_file_id'] is None:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Please upload a file first"
        })
    else:
        try:
            st.session_state.answer = stream_answer(question)
        except RuntimeError as e:
            st.error(str(e))

############## Session State setup ##############

if "last_processed_file_id" not in st.session_state:
    st.session_state["last_processed_file_id"] = None

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Please upload a file and ask your question."
    }]

if "answer" not in st.session_state:
    st.session_state["answer"] = None

############## UI ##############

st.title("Knowledge Chatbot", text_alignment="center")

file = st.file_uploader("Upload a file", type=["txt", "doc", "pdf", "md"])

if file:
    file_id = (file.name, file.size)
    if st.session_state["last_processed_file_id"] != file_id:
        try:
            save_file_content(file)
            st.session_state["last_processed_file_id"] = file_id
        except Exception as e:
            logger.exception("Failed to process or save uploaded file")
            st.error(f"Failed to process file: {e}")

with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if st.session_state.answer:
        text_answer = ""
        with st.chat_message("assistant"):
            text_answer = st.write_stream(st.session_state.answer, cursor="▌")

            st.session_state.messages.append({
                "role": "assistant",
                "content": text_answer
            })
            st.session_state.answer = None


st.chat_input("Your question:", key="user_question", on_submit=render_answer)
