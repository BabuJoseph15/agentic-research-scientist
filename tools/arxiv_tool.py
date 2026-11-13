"""
ArXiv Research Tool.

Retrieves research papers from arXiv
based on a research query.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.0
"""

from typing import List, Dict

import arxiv

from utils.cache_manager import (
    append_research_papers
)


MAX_RESULTS = 10


def search_arxiv(
    query: str,
    max_results: int = MAX_RESULTS
) -> List[Dict]:
    """
    Search research papers from arXiv.

    Args:
        query (str):
            Research question or topic.

        max_results (int):
            Maximum number of papers
            to retrieve.

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
                "link": result.entry_id
            }

            papers.append(paper)

        if papers:

            append_research_papers(
                papers
            )

            print(
                f"✅ Retrieved "
                f"{len(papers)} papers"
            )

        else:

            print(
                "⚠️ No papers found."
            )

        return papers

    except Exception as error:

        print(
            f"❌ ArXiv Search Failed: "
            f"{error}"
        )

        return []


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
            Formatted evidence summary.
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

Link:
{paper['link']}
"""
        )

    return "\n".join(summaries)


def extract_evidence(
    papers: List[Dict]
) -> str:
    """
    Extract evidence text from papers.

    This function is used by
    hypothesis and analysis agents
    when constructing prompts.

    Args:
        papers (List[Dict]):
            Retrieved papers.

    Returns:
        str:
            Concatenated paper summaries.
    """

    if not papers:
        return ""

    return "\n\n".join(
        [
            paper["summary"]
            for paper in papers
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
            f"Link: "
            f"{paper['link']}"
        )

        print(
            "-"
            * 80
        )