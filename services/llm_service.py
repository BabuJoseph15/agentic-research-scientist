"""
LLM Service.

Provides a reusable GPT-4o client
for workflow agents.

Author:
    Babu Guduru
"""

from langchain_openai import ChatOpenAI

from config.settings import (
    OPENAI_API_KEY,
    OPENAI_MODEL
)


llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=0.2
)