"""
Cache Manager.

Provides functionality for:

1. Research paper caching
2. Research history persistence
3. Cache retrieval
4. Cache updates

This module helps reduce external API calls
and maintains an audit trail of completed
research workflow executions.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.5
"""

import json

from pathlib import Path

from datetime import datetime

from utils.logger import logger


# ----------------------------------------------------------
# File Locations
# ----------------------------------------------------------

CACHE_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "cache"
    / "research_papers.json"
)

HISTORY_FILE = (
    Path(__file__).parent.parent
    / "reports"
    / "history"
    / "research_history.json"
)


# ----------------------------------------------------------
# Research Paper Cache
# ----------------------------------------------------------

def save_papers_to_cache(
    papers: list
) -> None:
    """
    Save research papers to cache.

    Args:
        papers (list):
            Retrieved Arxiv papers.

    Returns:
        None
    """

    try:

        cache_data = {
            "papers": papers,
            "last_updated": (
                datetime.now().isoformat()
            ),
            "source": "arxiv",
            "status": "success"
        }

        with open(
            CACHE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                cache_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        logger.info(
            "Research papers cached successfully."
        )

    except Exception as ex:

        logger.error(
            f"Failed saving cache: {str(ex)}"
        )


def load_papers_from_cache() -> list:
    """
    Load papers from cache.

    Returns:
        list:
            Cached papers.

            Empty list if cache unavailable.
    """

    try:

        if not CACHE_FILE.exists():

            logger.warning(
                "Research cache file not found."
            )

            return []

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            cache_data = json.load(file)

        logger.info(
            "Research papers loaded from cache."
        )

        return cache_data.get(
            "papers",
            []
        )

    except Exception as ex:

        logger.error(
            f"Failed loading cache: {str(ex)}"
        )

        return []


# ----------------------------------------------------------
# Research History
# ----------------------------------------------------------

def save_report_history(
    question: str,
    hypothesis: str,
    approval: str
) -> None:
    """
    Save completed research workflow
    results into history storage.

    Args:
        question (str):
            Research question.

        hypothesis (str):
            Generated hypothesis.

        approval (str):
            Human review decision.

    Returns:
        None
    """

    try:

        history_entry = {
            "timestamp":
            datetime.now().isoformat(),

            "question":
            question,

            "approval":
            approval,

            "hypothesis":
            hypothesis
        }

        if HISTORY_FILE.exists():

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                history_data = json.load(file)

        else:

            history_data = {
                "reports": []
            }

        history_data[
            "reports"
        ].append(
            history_entry
        )

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        logger.info(
            "Research history updated."
        )

    except Exception as ex:

        logger.error(
            f"Failed updating history: {str(ex)}"
        )


def load_report_history() -> list:
    """
    Load stored research history.

    Returns:
        list:
            Historical reports.
    """

    try:

        if not HISTORY_FILE.exists():

            return []

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            history_data = json.load(file)

        return history_data.get(
            "reports",
            []
        )

    except Exception as ex:

        logger.error(
            f"Failed loading history: {str(ex)}"
        )

        return []