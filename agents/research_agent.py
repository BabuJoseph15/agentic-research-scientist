from utils.logger import logger
from tools.arxiv_tool import search_arxiv


def research_agent(state):

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