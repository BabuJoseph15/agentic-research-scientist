"""
Research State Definition.

Defines the shared workflow state used by
all LangGraph agents.

The state acts as the central memory
container that is passed between workflow
nodes.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.7
"""

from typing import TypedDict


class ResearchState(TypedDict):
    """
    Shared workflow state.

    Attributes:
        question (str):
            Research question.

        papers (list):
            Research papers retrieved
            from ArXiv.

        evidence (list):
            Extracted evidence from
            research papers.

        analysis (dict):
            Statistical findings
            from the dataset.

        hypothesis (str):
            GPT-generated scientific
            hypothesis.

        approval (str):
            Human approval decision.

        report (str):
            Final approved report.

        pdf_path (str):
            Generated PDF file path.
    """

    question: str

    papers: list

    evidence: list

    analysis: dict

    hypothesis: str

    approval: str

    report: str

    pdf_path: str