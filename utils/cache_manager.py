"""
Cache Manager.

Provides functionality for:

1. Research paper caching
2. Research history persistence
3. Cache retrieval
4. Cache updates

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.8
"""

import json

from pathlib import Path

from datetime import datetime

from utils.logger import logger


# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent

CACHE_DIR = (
    PROJECT_ROOT
    / "data"
    / "cache"
)

HISTORY_DIR = (
    PROJECT_ROOT
    / "reports"
    / "history"
)

CACHE_FILE = (
    CACHE_DIR
    / "research_papers.json"
)

HISTORY_FILE = (
    HISTORY_DIR
    / "research_history.json"
)

CACHE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ----------------------------------------------------------
# Paper Cache
# ----------------------------------------------------------

def save_papers_to_cache(
    papers: list
) -> None:
    """
    Save research papers to cache.
    """

    try:

        cache_data = {
            "papers": papers,
            "last_updated":
            datetime.now().isoformat(),
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
            f"Cache save failed: {ex}"
        )


def load_papers_from_cache() -> list:
    """
    Load cached research papers.
    """

    try:

        if not CACHE_FILE.exists():
            return []

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            cache_data = json.load(file)

        logger.info(
            "Loaded papers from cache."
        )

        return cache_data.get(
            "papers",
            []
        )

    except Exception as ex:

        logger.error(
            f"Cache load failed: {ex}"
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
    Save completed workflow
    execution history.
    """

    try:

        entry = {
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

        if "reports" not in history_data:
            history_data["reports"] = []

        history_data[
            "reports"
        ].append(
            entry
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
            f"History update failed: {ex}"
        )


def load_report_history() -> list:
    """
    Load research history.
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
            f"History load failed: {ex}"
        )

        return []