def report_agent(state):

    if state["approval"].lower() != "yes":

        state["report"] = (
            "Report generation rejected."
        )

        return state

    report = f"""
FINAL RESEARCH REPORT

Question:
{state['question']}

Hypothesis:
{state['hypothesis']}

Status:
Approved
"""

    state["report"] = report

    return state