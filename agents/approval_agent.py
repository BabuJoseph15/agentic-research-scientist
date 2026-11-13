"""
Approval Agent.

Responsible for collecting human feedback
for generated scientific hypotheses.

Supports:

1. Console Approval
2. Streamlit Approval
3. Future LangGraph Interrupts

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.0
"""

from utils.logger import logger


def approval_agent(state):
    """
    Request human approval.

    If approval already exists in the
    workflow state, use that value.

    Otherwise prompt the user through
    the console.

    Args:
        state (dict):
            Current workflow state.

    Returns:
        dict:
            Updated workflow state.
    """

    logger.info(
        "Approval Agent Started"
    )

    #
    # Streamlit/UI Mode
    #
    existing_approval = (
        state.get(
            "approval",
            ""
        )
        .strip()
        .lower()
    )

    if existing_approval in [
        "yes",
        "no"
    ]:

        logger.info(
            f"Using supplied decision: "
            f"{existing_approval}"
        )

        return state

    #
    # Console Mode
    #
    print("\n")
    print("=" * 100)
    print("HUMAN REVIEW REQUIRED")
    print("=" * 100)

    print(
        "\nGenerated Hypothesis:\n"
    )

    print(
        state.get(
            "hypothesis",
            ""
        )
    )

    while True:

        approval = input(
            "\nApprove hypothesis? "
            "(yes/no): "
        ).strip().lower()

        if approval in [
            "yes",
            "no"
        ]:

            state["approval"] = (
                approval
            )

            print("\n")
            print("=" * 100)
            print(
                "REVIEW DECISION RECORDED"
            )
            print("=" * 100)

            print(
                f"Decision : "
                f"{approval.upper()}"
            )

            logger.info(
                f"Approval decision: "
                f"{approval}"
            )

            return state

        print(
            "\nInvalid input."
        )

        print(
            "Please enter "
            "'yes' or 'no'."
        )