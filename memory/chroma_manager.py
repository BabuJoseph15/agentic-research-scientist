"""
ChromaDB Memory Manager.

Stores and retrieves previous
research executions.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.2
"""

import uuid

from pathlib import Path

import chromadb

from utils.logger import logger


# --------------------------------------------------
# Chroma Database
# --------------------------------------------------

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


# --------------------------------------------------
# Save Memory
# --------------------------------------------------

def save_research_memory(
    question: str,
    hypothesis: str,
    report: str,
    approval: str
):
    """
    Save research workflow output.
    """

    try:

        document = f"""
Question:
{question}

Hypothesis:
{hypothesis}

Approval:
{approval}

Report:
{report}
"""

        collection.add(
            ids=[
                str(uuid.uuid4())
            ],
            documents=[
                document
            ],
            metadatas=[
                {
                    "question":
                    question,

                    "approval":
                    approval
                }
            ]
        )

        logger.info(
            "Research memory saved."
        )

    except Exception as ex:

        logger.error(
            f"Memory save failed: {ex}"
        )


# --------------------------------------------------
# Retrieve Similar Research
# --------------------------------------------------

def retrieve_similar_research(
    query: str,
    top_k: int = 3
):
    """
    Retrieve prior similar research.
    """

    try:

        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        return results

    except Exception as ex:

        logger.error(
            f"Memory retrieval failed: {ex}"
        )

        return None


# --------------------------------------------------
# Collection Stats
# --------------------------------------------------

def memory_count():
    """
    Number of stored research runs.
    """

    try:

        return collection.count()

    except Exception:

        return 0