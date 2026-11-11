
"""Retrieve dataset observations relevant to the research question."""

from tools.dataset_rag_tool import retrieve_dataset_context


def dataset_rag_agent(state):
    """Find relevant dataset rows and store their text and scores in workflow state."""
    results = retrieve_dataset_context(
        query=state["question"],
        top_k=3,
    )