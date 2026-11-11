"""
Research Agent.

Responsible for collecting academic evidence
from external scientific literature sources.

Workflow:
Question -> Arxiv Search -> Research Papers

Author: Babu Guduru
"""

from tools.arxiv_tool import (
    search_arxiv
)

from utils.logger import logger


def research_agent(state):
    """
    Execute research paper discovery.

    Args:
        state (dict):
            LangGraph workflow state.

    Returns:
        dict:
            Updated workflow state containing papers.
    """

    logger.info(
        "Research Agent Started"
    )

    papers = search_arxiv(
        state["question"]
    )

    logger.info(
        f"Found {len(papers)} papers"
    )

    state["papers"] = papers

    return state