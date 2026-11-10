from graph.workflow import graph


def main():

    initial_state = {
        "question": "Can climate change increase dengue outbreaks in India?",
        "papers": [],
        "evidence": [],
        "analysis": {}
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 100)
    print("RESEARCH PAPERS FOUND")
    print("=" * 100)

    for idx, paper in enumerate(result["papers"], start=1):

        print(f"\nPaper {idx}")
        print("-" * 100)
        print(f"Title      : {paper['title']}")
        print(f"Published  : {paper['published']}")
        print(f"Authors    : {', '.join(paper['authors'])}")
        print(f"URL        : {paper['url']}")

    print("\n" + "=" * 100)
    print("EVIDENCE EXTRACTED")
    print("=" * 100)

    for idx, evidence in enumerate(result["evidence"], start=1):

        print(f"\nEvidence {idx}")
        print(f"Title      : {evidence['title']}")
        print(f"Published  : {evidence['published']}")

    print("\n" + "=" * 100)
    print("CORRELATION ANALYSIS")
    print("=" * 100)

    if result["analysis"]:
        for feature, correlation in result["analysis"].items():

            print(
                f"{feature:<25} : {correlation}"
            )
    else:
        print("No analysis results available.")


if __name__ == "__main__":
    main()