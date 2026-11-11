"""
Evidence Agent.

Converts retrieved papers into structured
evidence records that can be consumed
by downstream analytical agents.

Author: Babu Guduru
"""


def evidence_agent(state):
    """
    Extract evidence from research papers.

    Args:
        state (dict):
            Current workflow state.

    Returns:
        dict:
            Updated workflow state containing evidence.
    """

    papers = state["papers"]

    evidence = []

    for paper in papers:

        evidence.append(
            {
                "title": paper["title"],
                "published": paper["published"]
            }
        )

    state["evidence"] = evidence

    return state