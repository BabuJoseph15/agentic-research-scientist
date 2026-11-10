def approval_agent(state):

    print("\n")
    print("=" * 100)
    print("HUMAN REVIEW REQUIRED")
    print("=" * 100)

    print(state["hypothesis"])

    approval = input(
        "\nApprove hypothesis? (yes/no): "
    )

    state["approval"] = approval

    return state