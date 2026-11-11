"""
Research State Definition.

Shared state object used throughout
the LangGraph workflow.

Author:
    Babu Guduru
"""

from typing import TypedDict


class ResearchState(TypedDict):
    """
    Shared workflow state.

    Attributes:
        question:
            Research question.

        papers:
            Retrieved research papers.

        evidence:
            Extracted evidence.

        analysis:
            Statistical findings.

        hypothesis:
            Generated scientific hypothesis.

        approval:
            Human approval decision.
    """

    question: str
    papers: list
    evidence: list
    analysis: dict
    hypothesis: str
    approval: str
    report: str