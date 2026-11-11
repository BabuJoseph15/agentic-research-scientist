"""
Arxiv Literature Search Tool.

This module provides functionality to search academic
research papers from Arxiv and return structured
metadata required by the Research Agent.

Author: Babu Guduru
Project: Agentic Research Scientist
"""

import arxiv


def search_arxiv(
    query: str,
    max_results: int = 5
):
    """
    Search Arxiv for research papers.

    Args:
        query (str):
            Research question or search keyword.

        max_results (int):
            Maximum number of papers to retrieve.

    Returns:
        list:
            List of dictionaries containing paper details.
    """

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    for paper in client.results(search):

        papers.append(
            {
                "title": paper.title,
                "authors": [
                    author.name
                    for author in paper.authors
                ],
                "summary": paper.summary,
                "published": str(
                    paper.published.date()
                ),
                "url": str(
                    paper.entry_id
                )
            }
        )

    return papers