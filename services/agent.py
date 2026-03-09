"""LLM Module"""

import os
from langchain_openai import ChatOpenAI


def ask_agent(prompt):
    """Invoke the LLM with the given prompt. Model is configurable via OPENAI_MODEL."""
    model = ChatOpenAI(model=os.environ.get('OPENAI_MODEL', 'gpt-4o-mini'))
    return model.invoke(prompt)
