"""
Arxiv Literature Search Tool.
"""

import arxiv

from utils.logger import logger


def search_arxiv(
    query: str,
    max_results: int = 5
):
    """
    Search research papers from Arxiv.

    Args:
        query (str):
            Research question.

        max_results (int):
            Number of papers to retrieve.

    Returns:
        list:
            Retrieved papers.
    """

    papers = []

    try:

        client = arxiv.Client()

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

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

    except Exception as ex:

        logger.error(
            f"Arxiv search failed: {str(ex)}"
        )

        papers.append(
            {
                "title": "Arxiv API Unavailable",
                "authors": [],
                "summary": (
                    "Research papers could not "
                    "be retrieved due to API "
                    "rate limiting."
                ),
                "published": "N/A",
                "url": "N/A"
            }
        )

    return papers