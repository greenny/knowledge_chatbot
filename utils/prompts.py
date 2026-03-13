"""Prompt Templates"""
from langchain_core.prompts import ChatPromptTemplate


PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}
---
Answer the question based on the above context: {question}
Use the provided context if it is relevant.

If the context does not contain the answer,
use your general knowledge.
"""

def build_prompt(results, question):
    """Use chunks and user question to build prompt template"""
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    return prompt_template.format(context=context_text, question=question)
