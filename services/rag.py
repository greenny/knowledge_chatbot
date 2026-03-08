import logging

import data.vector_store as vstore
from utils.prompts import build_prompt

from services.agent import ask_agent

logger = logging.getLogger(__name__)


def answer(question):
  """
  Answer a question using RAG: retrieve relevant chunks, build prompt, call LLM.
  Raises RuntimeError with a user-facing message on retrieval or LLM failure.
  """
  try:
    results = vstore.query_db(question)
  except Exception as e:
    logger.exception('Vector store query failed')
    raise RuntimeError('Search failed. Please try again.') from e

  if len(results) == 0 or results[0][1] < 0.6:
    return 'Unable to find matching results.'

  try:
    prompt = build_prompt(results, question)
    response = ask_agent(prompt)
    return response.content
  except Exception as e:
    logger.exception('LLM call failed')
    raise RuntimeError('AI request failed. Check your API key and connection.') from e
