def evidence_agent(state):

    papers = state["papers"]

    evidence = []

    for paper in papers:

        evidence.append(
            {
                "title": paper["title"],
                "published": paper["published"]
            }
        )

    state["evidence"] = evidence

    return state