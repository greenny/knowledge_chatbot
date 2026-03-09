"""Main entry point for the Knowledge Chatbot application."""

import logging
import os

import streamlit as st
from dotenv import load_dotenv

from services.ingestion import save_file_content
from services.rag import answer

logger = logging.getLogger(__name__)

############## Preparations ##############
load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')
if not api_key or not api_key.strip():
    st.error('OPENAI_API_KEY is not set. Add it to your .env file (see .env.simple).')
    st.stop()
os.environ['OPENAI_API_KEY'] = api_key


def render_question_input(question_number=1):
    """Creates the question input and renderd an answer."""
    with st.chat_message('assistant'):
        st.write('Ask a question or clear the file input.')
    with st.chat_message('user'):
        question = st.text_input('Question:', key=f"text_input_{question_number}")
    if question:
        with st.chat_message('assistant'):
            try:
                st.write(answer(question))
            except RuntimeError as e:
                st.error(str(e))
        render_question_input(question_number + 1)

############## UI ##############

st.title('Knowledge Chatbot', text_alignment='center')

if 'last_processed_file_id' not in st.session_state:
    st.session_state['last_processed_file_id'] = None

file = st.file_uploader('Upload a file', type=['txt', 'doc', 'pdf', 'md'])

if file:
    file_id = (file.name, file.size)
    if st.session_state['last_processed_file_id'] != file_id:
        try:
            save_file_content(file)
            st.session_state['last_processed_file_id'] = file_id
        except Exception as e:
            logger.exception('Failed to process or save uploaded file')
            st.error(f"Failed to process file: {e}")
    render_question_input()
