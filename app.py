"""
Agentic Research Scientist Application.

This is the main entry point for executing the
LangGraph workflow.

Workflow:

    Research Agent
          ↓
    Evidence Agent
          ↓
    Analysis Agent
          ↓
    Hypothesis Agent
          ↓
    Approval Agent
          ↓
         END

Responsibilities:

1. Initialize workflow state.
2. Invoke LangGraph workflow.
3. Display research papers.
4. Display extracted evidence.
5. Display statistical findings.
6. Display generated hypothesis.
7. Display approval decision.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.2
"""

from graph.workflow import graph


def main():
    """
    Execute the LangGraph workflow.

    Creates the initial workflow state,
    invokes the workflow, and prints the
    outputs produced by each agent.

    Returns:
        None
    """

    # ----------------------------------------------------------
    # Initialize Workflow State
    # ----------------------------------------------------------
    initial_state = {
        "question": (
            "Can climate change increase dengue "
            "outbreaks in India?"
        ),
        "papers": [],
        "evidence": [],
        "analysis": {},
        "hypothesis": "",
        "approval": ""
    }

    # ----------------------------------------------------------
    # Execute Workflow
    # ----------------------------------------------------------
    result = graph.invoke(initial_state)

    # ----------------------------------------------------------
    # Research Papers
    # ----------------------------------------------------------
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

    # ----------------------------------------------------------
    # Evidence
    # ----------------------------------------------------------
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

    # ----------------------------------------------------------
    # Statistical Analysis
    # ----------------------------------------------------------
    print("\n" + "=" * 100)
    print("CORRELATION ANALYSIS")
    print("=" * 100)

    if result["analysis"]:

        for feature, correlation in (
            result["analysis"].items()
        ):

            print(
                f"{feature:<25} : "
                f"{correlation}"
            )

    else:

        print(
            "No analysis results available."
        )

    # ----------------------------------------------------------
    # Generated Hypothesis
    # ----------------------------------------------------------
    print("\n" + "=" * 100)
    print("HYPOTHESIS")
    print("=" * 100)

    print(result["hypothesis"])

    # ----------------------------------------------------------
    # Approval Status
    # ----------------------------------------------------------
    print("\n" + "=" * 100)
    print("APPROVAL STATUS")
    print("=" * 100)

    print(
        f"Decision : "
        f"{result['approval'].upper()}"
    )


if __name__ == "__main__":
    main()