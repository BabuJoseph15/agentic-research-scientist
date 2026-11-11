"""
Approval Agent.

Responsible for collecting human feedback on the
generated scientific hypothesis before allowing
the workflow to proceed to report generation.

This agent represents the first Human-in-the-Loop
(HITL) checkpoint in the Agentic Research Scientist
workflow.

Workflow:

    Hypothesis
         ↓
    Human Review
         ↓
    Approve / Reject
         ↓
    Report Generation

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.2
"""


def approval_agent(state):
    """
    Request human approval for the generated hypothesis.

    Displays the generated hypothesis and waits
    for reviewer input.

    Accepted Inputs:
        - yes
        - no

    Args:
        state (dict):
            Current LangGraph workflow state.

    Returns:
        dict:
            Updated state containing approval decision.
    """

    print("\n")
    print("=" * 100)
    print("HUMAN REVIEW REQUIRED")
    print("=" * 100)

    print("\nGenerated Hypothesis:\n")
    print(state["hypothesis"])

    while True:

        approval = input(
            "\nApprove hypothesis? (yes/no): "
        ).strip().lower()

        if approval in ["yes", "no"]:

            state["approval"] = approval

            print("\n")
            print("=" * 100)
            print("REVIEW DECISION RECORDED")
            print("=" * 100)
            print(f"Decision : {approval.upper()}")

            return state

        print(
            "\nInvalid input."
            "\nPlease enter either 'yes' or 'no'."
        )