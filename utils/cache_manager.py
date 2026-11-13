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
    0.7
"""

import json

from pathlib import Path

from datetime import datetime

from utils.logger import logger


# ----------------------------------------------------------
# File Locations
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent

CACHE_DIR = PROJECT_ROOT / "data" / "cache"

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

# Ensure directories exist
CACHE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
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
            List of research papers.

    Returns:
        None
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
            f"Failed saving cache: {str(ex)}"
        )


def load_papers_from_cache() -> list:
    """
    Load research papers from cache.

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
    Save workflow execution history.

    Args:
        question (str):
            Research question.

        hypothesis (str):
            Generated hypothesis.

        approval (str):
            Approval decision.

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

        #
        # Load existing history
        #
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

        #
        # Repair corrupted structure
        #
        if not isinstance(
            history_data,
            dict
        ):
            history_data = {
                "reports": []
            }

        if "reports" not in history_data:

            history_data["reports"] = []

        #
        # Add new entry
        #
        history_data[
            "reports"
        ].append(
            history_entry
        )

        #
        # Save updated history
        #
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
            f"Failed updating history: "
            f"{str(ex)}"
        )


def load_report_history() -> list:
    """
    Load workflow history.

    Returns:
        list:
            Historical workflow executions.
    """

    try:

        if not HISTORY_FILE.exists():

            logger.warning(
                "Research history file not found."
            )

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
            f"Failed loading history: "
            f"{str(ex)}"
        )

        return []


# ----------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------

def clear_paper_cache() -> None:
    """
    Delete cached research papers.

    Returns:
        None
    """

    try:

        if CACHE_FILE.exists():

            CACHE_FILE.unlink()

            logger.info(
                "Research cache cleared."
            )

    except Exception as ex:

        logger.error(
            f"Failed clearing cache: "
            f"{str(ex)}"
        )


def get_cache_metadata() -> dict:
    """
    Retrieve cache metadata.

    Returns:
        dict:
            Cache metadata.
    """

    try:

        if not CACHE_FILE.exists():

            return {}

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            cache_data = json.load(file)

        return {
            "last_updated":
            cache_data.get(
                "last_updated"
            ),

            "source":
            cache_data.get(
                "source"
            ),

            "status":
            cache_data.get(
                "status"
            ),

            "paper_count":
            len(
                cache_data.get(
                    "papers",
                    []
                )
            )
        }

    except Exception as ex:

        logger.error(
            f"Failed reading cache metadata: "
            f"{str(ex)}"
        )

        return {}