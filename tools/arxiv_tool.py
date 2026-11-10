import arxiv


def search_arxiv(query: str, max_results: int = 5):

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    for paper in client.results(search):

        papers.append(
            {
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "summary": paper.summary,
                "published": str(paper.published.date()),
                "url": str(paper.entry_id)
            }
        )

    return papers