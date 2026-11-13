"""
Cache Manager.

Handles persistent storage for:

1. Research history
2. Retrieved research papers
3. Cached workflow data

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.0
"""

import json
import os
from datetime import datetime


REPORTS_DIR = "reports"

RESEARCH_HISTORY_FILE = os.path.join(
    REPORTS_DIR,
    "research_history.json"
)

RESEARCH_PAPERS_FILE = os.path.join(
    REPORTS_DIR,
    "research_papers.json"
)


def ensure_reports_directory() -> None:
    """
    Create reports directory if it does not exist.
    """

    os.makedirs(
        REPORTS_DIR,
        exist_ok=True
    )


def initialize_cache_files() -> None:
    """
    Initialize cache files if they do not exist.
    """

    ensure_reports_directory()

    if not os.path.exists(
        RESEARCH_HISTORY_FILE
    ):

        with open(
            RESEARCH_HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )

    if not os.path.exists(
        RESEARCH_PAPERS_FILE
    ):

        with open(
            RESEARCH_PAPERS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


def load_research_history() -> list:
    """
    Load previous research runs.

    Returns:
        list:
            Research history records.
    """

    initialize_cache_files()

    try:

        with open(
            RESEARCH_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_report_history(
    question: str,
    hypothesis: str,
    approval: str
) -> None:
    """
    Save completed research report metadata.

    Args:
        question (str):
            Research question.

        hypothesis (str):
            Generated hypothesis.

        approval (str):
            Approval decision.
    """

    history = load_research_history()

    history.append(
        {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "question": question,
            "hypothesis": hypothesis,
            "approval": approval
        }
    )

    with open(
        RESEARCH_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_research_papers() -> list:
    """
    Load cached research papers.

    Returns:
        list:
            Cached paper records.
    """

    initialize_cache_files()

    try:

        with open(
            RESEARCH_PAPERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_research_papers(
    papers: list
) -> None:
    """
    Save retrieved research papers.

    Args:
        papers (list):
            List of paper dictionaries.
    """

    initialize_cache_files()

    with open(
        RESEARCH_PAPERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            papers,
            file,
            indent=4,
            ensure_ascii=False
        )


def append_research_papers(
    new_papers: list
) -> None:
    """
    Append newly retrieved papers
    while preventing duplicates.

    Args:
        new_papers (list):
            Newly retrieved paper records.
    """

    existing_papers = load_research_papers()

    existing_titles = {
        paper.get(
            "title",
            ""
        ).lower()
        for paper in existing_papers
    }

    for paper in new_papers:

        title = paper.get(
            "title",
            ""
        ).lower()

        if title not in existing_titles:

            existing_papers.append(
                paper
            )

            existing_titles.add(
                title
            )

    save_research_papers(
        existing_papers
    )


def get_cache_statistics() -> dict:
    """
    Get cache statistics.

    Returns:
        dict:
            Statistics summary.
    """

    history = load_research_history()

    papers = load_research_papers()

    return {
        "research_runs": len(history),
        "cached_papers": len(papers),
        "history_file": RESEARCH_HISTORY_FILE,
        "papers_file": RESEARCH_PAPERS_FILE
    }


# Initialize cache structure when module loads
initialize_cache_files()