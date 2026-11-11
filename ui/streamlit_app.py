"""
Streamlit User Interface.

Provides a web-based interface for interacting
with the Agentic Research Scientist workflow.

Features:
    - Enter research questions
    - Execute LangGraph workflow
    - Display research papers
    - Display statistical analysis
    - Display GPT-generated hypothesis
    - Display final report

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.4
"""

import streamlit as st

from graph.workflow import graph


def initialize_state():
    """
    Create initial workflow state.

    Returns:
        dict:
            Initial LangGraph state.
    """

    return {
        "question": "",
        "papers": [],
        "evidence": [],
        "analysis": {},
        "hypothesis": "",
        "approval": "",
        "report": ""
    }


def run_workflow(question: str):
    """
    Execute LangGraph workflow.

    Args:
        question (str):
            User research question.

    Returns:
        dict:
            Workflow result.
    """

    state = initialize_state()

    state["question"] = question

    result = graph.invoke(state)

    return result


def main():
    """
    Streamlit application entry point.
    """

    st.set_page_config(
        page_title="Agentic Research Scientist",
        page_icon="🔬",
        layout="wide"
    )

    st.title("🔬 Agentic Research Scientist")

    st.markdown(
        """
        Generate research hypotheses using:

        - Arxiv Literature Search
        - Statistical Analysis
        - GPT-4o Reasoning
        - Human Review
        - Automated Reports
        """
    )

    question = st.text_area(
        label="Research Question",
        placeholder=(
            "Can climate change increase "
            "dengue outbreaks in India?"
        ),
        height=100
    )

    run_button = st.button(
        "Generate Research Report"
    )

    if run_button:

        if not question:

            st.warning(
                "Please enter a research question."
            )
            return

        with st.spinner(
            "Running Agentic Workflow..."
        ):

            result = run_workflow(question)

        st.success(
            "Workflow Completed Successfully"
        )

        # --------------------------------------------------
        # Papers
        # --------------------------------------------------

        st.header("📚 Research Papers")

        for paper in result["papers"]:

            with st.expander(
                paper["title"]
            ):

                st.write(
                    f"**Published:** "
                    f"{paper['published']}"
                )

                st.write(
                    f"**Authors:** "
                    f"{', '.join(paper['authors'])}"
                )

                st.write(
                    f"**URL:** "
                    f"{paper['url']}"
                )

        # --------------------------------------------------
        # Analysis
        # --------------------------------------------------

        st.header("📊 Statistical Findings")

        st.json(
            result["analysis"]
        )

        # --------------------------------------------------
        # Hypothesis
        # --------------------------------------------------

        st.header("🧠 GPT-Generated Hypothesis")

        st.write(
            result["hypothesis"]
        )

        # --------------------------------------------------
        # Approval
        # --------------------------------------------------

        st.header("✅ Review")

        approval = st.radio(
            "Do you approve this hypothesis?",
            (
                "Approve",
                "Reject"
            )
        )

        if st.button(
            "Submit Review"
        ):

            st.success(
                f"Decision Submitted: {approval}"
            )

        # --------------------------------------------------
        # Report
        # --------------------------------------------------

        st.header("📄 Final Report")

        st.text_area(
            label="Report",
            value=result["report"],
            height=400
        )


if __name__ == "__main__":
    main()