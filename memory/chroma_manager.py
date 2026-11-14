"""
ChromaDB Memory Manager.

Stores and retrieves historical
research executions.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.1
"""

import uuid

import chromadb

from pathlib import Path

from utils.logger import logger


CHROMA_PATH = (
    Path(__file__).parent
    / "chroma_db"
)

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="research_memory"
)


def save_research_memory(
    question: str,
    hypothesis: str,
    report: str,
    approval: str
):
    """
    Save research result into memory.
    """

    try:

        collection.add(
            ids=[
                str(uuid.uuid4())
            ],
            documents=[
                report
            ],
            metadatas=[
                {
                    "question": question,
                    "approval": approval
                }
            ]
        )

        logger.info(
            "Research memory saved."
        )

    except Exception as ex:

        logger.error(
            f"Chroma save failed: {ex}"
        )


def retrieve_similar_research(
    query: str,
    top_k: int = 3
):
    """
    Retrieve similar research.
    """

    try:

        result = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        return result

    except Exception as ex:

        logger.error(
            f"Chroma retrieval failed: {ex}"
        )

        return None


def memory_count():
    """
    Number of stored memories.
    """

    return collection.count()