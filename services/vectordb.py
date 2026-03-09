"""Module providing vector store functions."""

import logging
import os

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)

CHROMA_PATH = os.environ.get('CHROMA_PATH', 'chroma')


def save_to_db(chunks):
    """Function saving chunks to the DB."""
    try:
        Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH)
        logger.info("Saved %d chunks to %s", len(chunks), CHROMA_PATH)
    except Exception:
        logger.exception('Failed to save chunks to vector store')
        raise


def query_db(question):
    """Function querying the DB."""
    try:
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        return db.similarity_search_with_relevance_scores(question, k=3)
    except Exception:
        logger.exception('Failed to query vector store')
        raise
