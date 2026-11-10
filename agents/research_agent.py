from tools.arxiv_tool import search_arxiv


def research_agent(state):

    papers = search_arxiv(
        state["question"]
    )

    state["papers"] = papers

    return state