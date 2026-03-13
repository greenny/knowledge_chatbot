"""LLM Module"""

import os
from functools import lru_cache
from langchain_openai import ChatOpenAI

@lru_cache(maxsize=1)
def get_model():
    """Initialize or returns the model. It is configurable via OPENAI_MODEL."""
    return ChatOpenAI(model=os.environ.get('OPENAI_MODEL', 'gpt-4o-mini'), temperature=0)

def ask_agent(prompt):
    """Invoke the LLM with the given prompt."""
    return get_model().stream(prompt)
