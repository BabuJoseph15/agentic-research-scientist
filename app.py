"""
Agentic Research Scientist.

Application entry point.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.6
"""

from graph.workflow import graph


def main():
    """
    Execute workflow.

    Returns:
        None
    """

    initial_state = {
        "question": (
            "Can climate change increase "
            "dengue outbreaks in India?"
        ),
        "papers": [],
        "evidence": [],
        "analysis": {},
        "hypothesis": "",
        "approval": "",
        "report": ""
    }

    result = graph.invoke(initial_state)

    # --------------------------------------------------
    # Research Papers
    # --------------------------------------------------

    print("\n" + "=" * 100)
    print("RESEARCH PAPERS FOUND")
    print("=" * 100)

    for idx, paper in enumerate(
        result["papers"],
        start=1
    ):

        print(f"\nPaper {idx}")
        print("-" * 100)

        print(
            f"Title      : {paper['title']}"
        )

        print(
            f"Published  : {paper['published']}"
        )

        print(
            f"Authors    : "
            f"{', '.join(paper['authors'])}"
        )

        print(
            f"URL        : {paper['url']}"
        )

    # --------------------------------------------------
    # Evidence
    # --------------------------------------------------

    print("\n" + "=" * 100)
    print("EVIDENCE EXTRACTED")
    print("=" * 100)

    for idx, evidence in enumerate(
        result["evidence"],
        start=1
    ):

        print(f"\nEvidence {idx}")

        print(
            f"Title      : "
            f"{evidence['title']}"
        )

        print(
            f"Published  : "
            f"{evidence['published']}"
        )

    # --------------------------------------------------
    # Analysis
    # --------------------------------------------------

    print("\n" + "=" * 100)
    print("CORRELATION ANALYSIS")
    print("=" * 100)

    for feature, correlation in (
        result["analysis"].items()
    ):

        print(
            f"{feature:<25} : "
            f"{correlation}"
        )

    # --------------------------------------------------
    # Hypothesis
    # --------------------------------------------------

    print("\n" + "=" * 100)
    print("GPT GENERATED HYPOTHESIS")
    print("=" * 100)

    print(
        result["hypothesis"]
    )

    # --------------------------------------------------
    # Approval
    # --------------------------------------------------

    print("\n" + "=" * 100)
    print("APPROVAL STATUS")
    print("=" * 100)

    print(
        f"Decision : "
        f"{result['approval'].upper()}"
    )

    # --------------------------------------------------
    # Final Report
    # --------------------------------------------------

    print("\n" + "=" * 100)
    print("FINAL REPORT")
    print("=" * 100)

    print(
        result["report"]
    )


if __name__ == "__main__":
    main()