"""
Approval Agent.

Responsible for collecting human feedback on the
generated scientific hypothesis before allowing
report generation.

This agent represents the first Human-in-the-Loop
(HITL) checkpoint in the workflow.

Workflow:

    Hypothesis
         ↓
    Human Review
         ↓
    Approve / Reject
         ↓
    Updated State

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

    The agent displays the hypothesis and waits for
    user input before continuing the workflow.

    Args:
        state (dict):
            Current LangGraph workflow state.

    Returns:
        dict:
            Updated workflow state containing the
            approval decision.

    State Updates:
        approval:
            Human review decision.
            Expected values:
                - yes
                - no
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
            break

        print(
            "\nInvalid input. Please enter 'yes' or 'no'."
        )

    state["approval"] = approval

    return state