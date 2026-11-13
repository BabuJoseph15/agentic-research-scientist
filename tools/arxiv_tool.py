"""
ArXiv Research Tool.

Retrieves research papers from ArXiv
based on a research query.

Features:

1. Live ArXiv retrieval
2. Local cache storage
3. Cache recovery during API failures
4. Evidence extraction utilities

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.1
"""

from typing import List, Dict

import arxiv

from utils.logger import logger

from utils.cache_manager import (
    save_papers_to_cache,
    load_papers_from_cache
)


MAX_RESULTS = 10


def search_arxiv(
    query: str,
    max_results: int = MAX_RESULTS
) -> List[Dict]:
    """
    Search research papers from ArXiv.

    Args:
        query (str):
            Research question or topic.

        max_results (int):
            Maximum number of papers to retrieve.

    Returns:
        List[Dict]:
            Research paper metadata.
    """

    print(
        f"\n🔍 Searching ArXiv for: {query}"
    )

    papers = []

    try:

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        client = arxiv.Client()

        for result in client.results(search):

            paper = {
                "title": result.title,
                "authors": [
                    author.name
                    for author in result.authors
                ],
                "published": (
                    result.published.strftime(
                        "%Y-%m-%d"
                    )
                    if result.published
                    else "Unknown"
                ),
                "summary": result.summary,
                "url": str(result.entry_id)
            }

            papers.append(paper)

        if papers:

            save_papers_to_cache(
                papers
            )

            logger.info(
                "Research papers cached successfully."
            )

            print(
                f"✅ Retrieved "
                f"{len(papers)} papers"
            )

        else:

            logger.warning(
                "No papers returned by ArXiv."
            )

        return papers

    except Exception as error:

        logger.error(
            f"ArXiv Search Failed: {error}"
        )

        print(
            f"❌ ArXiv Search Failed: {error}"
        )

        cached_papers = (
            load_papers_from_cache()
        )

        if cached_papers:

            logger.info(
                "Using cached papers."
            )

            print(
                f"📦 Using "
                f"{len(cached_papers)} "
                f"cached papers."
            )

            return cached_papers

        logger.warning(
            "No cached papers available."
        )

        return [
            {
                "title":
                "ArXiv API Unavailable",

                "authors":
                [],

                "published":
                "N/A",

                "summary":
                (
                    "Research papers could not "
                    "be retrieved and no cache "
                    "is available."
                ),

                "url":
                "N/A"
            }
        ]


def format_paper_summary(
    papers: List[Dict]
) -> str:
    """
    Convert papers into formatted text.

    Args:
        papers (List[Dict]):
            Research papers.

    Returns:
        str:
            Formatted paper summary.
    """

    if not papers:

        return "No papers available."

    summaries = []

    for index, paper in enumerate(
        papers,
        start=1
    ):

        summaries.append(
            f"""
Paper {index}

Title:
{paper['title']}

Published:
{paper['published']}

Authors:
{", ".join(paper['authors'])}

Summary:
{paper['summary'][:500]}

URL:
{paper['url']}
"""
        )

    return "\n".join(
        summaries
    )


def extract_evidence(
    papers: List[Dict]
) -> str:
    """
    Extract evidence text from papers.

    Args:
        papers (List[Dict]):
            Retrieved research papers.

    Returns:
        str:
            Combined evidence text.
    """

    if not papers:

        return ""

    return "\n\n".join(
        [
            paper["summary"]
            for paper in papers
            if paper.get("summary")
        ]
    )


if __name__ == "__main__":

    topic = (
        "Climate change and dengue fever"
    )

    papers = search_arxiv(
        topic,
        max_results=5
    )

    print(
        "\n========== RESULTS =========="
    )

    for paper in papers:

        print(
            f"\nTitle: {paper['title']}"
        )

        print(
            f"Published: "
            f"{paper['published']}"
        )

        print(
            f"URL: "
            f"{paper['url']}"
        )

        print(
            "-" * 80
        )