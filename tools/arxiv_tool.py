"""
Arxiv Literature Search Tool.

Provides functionality for retrieving
scientific research papers from Arxiv.

Features:

1. Live Arxiv Retrieval
2. Local Cache Storage
3. Cache Recovery During API Failures
4. Structured Paper Metadata

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.5
"""

import arxiv

from utils.logger import logger

from utils.cache_manager import (
    save_papers_to_cache,
    load_papers_from_cache
)


def search_arxiv(
    query: str,
    max_results: int = 5
) -> list:
    """
    Retrieve research papers from Arxiv.

    Args:
        query (str):
            Research question.

        max_results (int):
            Maximum papers to retrieve.

    Returns:
        list:
            Research paper metadata.
    """

    papers = []

    try:

        logger.info(
            "Starting Arxiv search."
        )

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

        # Save Response Locally
        save_papers_to_cache(
            papers
        )

        logger.info(
            f"Successfully retrieved "
            f"{len(papers)} papers."
        )

        return papers

    except Exception as ex:

        logger.error(
            f"Arxiv search failed: {str(ex)}"
        )

        # Attempt Cache Recovery
        cached_papers = (
            load_papers_from_cache()
        )

        if cached_papers:

            logger.info(
                "Using cached research papers."
            )

            return cached_papers

        logger.warning(
            "No cached papers available."
        )

        papers.append(
            {
                "title":
                "Arxiv API Unavailable",

                "authors": [],

                "summary":
                (
                    "Research papers could "
                    "not be retrieved."
                ),

                "published":
                "N/A",

                "url":
                "N/A"
            }
        )

        return papers