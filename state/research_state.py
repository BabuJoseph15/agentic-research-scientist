"""
Research State Definition.

Central state container used by LangGraph
for passing information between agents.

Author: Babu Guduru
"""

from typing import TypedDict


class ResearchState(TypedDict):
    """
    Shared workflow state.

    Attributes:
        question:
            Research question.

        papers:
            Retrieved literature.

        evidence:
            Extracted evidence.

        analysis:
            Statistical findings.

        hypothesis:
            Generated hypothesis.
    """

    question: str
    papers: list
    evidence: list
    analysis: dict
    hypothesis: str