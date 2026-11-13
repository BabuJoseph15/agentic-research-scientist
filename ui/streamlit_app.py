"""
Streamlit User Interface.

Provides a web-based interface for interacting
with the Agentic Research Scientist workflow.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.0
"""

import sys
import os

from pathlib import Path

import streamlit as st


# --------------------------------------------------
# Project Root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


# --------------------------------------------------
# Imports
# --------------------------------------------------

from graph.workflow import graph

from agents.report_agent import (
    report_agent
)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def initialize_state():
    """
    Create initial workflow state.
    """

    return {
        "question": "",
        "papers": [],
        "evidence": [],
        "analysis": {},
        "hypothesis": "",
        "approval": "",
        "report": "",
        "pdf_path": ""
    }


def run_workflow(question: str):
    """
    Execute workflow.

    Args:
        question (str):
            Research question.

    Returns:
        dict:
            Workflow result.
    """

    state = initialize_state()

    state["question"] = question

    return graph.invoke(state)


# --------------------------------------------------
# Main UI
# --------------------------------------------------

def main():

    st.set_page_config(
        page_title="Agentic Research Scientist",
        page_icon="🔬",
        layout="wide"
    )

    st.title(
        "🔬 Agentic Research Scientist"
    )

    st.markdown(
        """
Generate research insights using:

- ArXiv Research Retrieval
- Statistical Analysis
- GPT-4o Scientific Reasoning
- Human Review
- PDF Report Generation
"""
    )

    # --------------------------------------------------
    # Research Question
    # --------------------------------------------------

    question = st.text_area(
        label="Research Question",
        value=(
            "Can climate change increase "
            "dengue outbreaks in India?"
        ),
        height=120
    )

    # --------------------------------------------------
    # Run Workflow
    # --------------------------------------------------

    if st.button(
        "🚀 Generate Research Analysis"
    ):

        with st.spinner(
            "Running Agentic Workflow..."
        ):

            result = run_workflow(
                question
            )

        st.session_state[
            "workflow_result"
        ] = result

        st.success(
            "Research analysis completed."
        )

    # --------------------------------------------------
    # Wait Until Data Exists
    # --------------------------------------------------

    if (
        "workflow_result"
        not in st.session_state
    ):
        return

    result = st.session_state[
        "workflow_result"
    ]

    # --------------------------------------------------
    # Papers
    # --------------------------------------------------

    st.header(
        "📚 Research Papers"
    )

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

    st.header(
        "📊 Statistical Findings"
    )

    st.json(
        result["analysis"]
    )

    # --------------------------------------------------
    # Hypothesis
    # --------------------------------------------------

    st.header(
        "🧠 GPT Scientific Analysis"
    )

    st.text_area(
        label="Generated Hypothesis",
        value=result["hypothesis"],
        height=450
    )

    # --------------------------------------------------
    # Human Approval
    # --------------------------------------------------

    st.header(
        "✅ Human Review"
    )

    decision = st.radio(
        "Review Decision",
        [
            "Approve",
            "Reject"
        ]
    )

    if st.button(
        "Submit Review"
    ):

        result["approval"] = (
            "yes"
            if decision == "Approve"
            else "no"
        )

        result = report_agent(
            result
        )

        st.session_state[
            "workflow_result"
        ] = result

        st.success(
            f"Hypothesis {decision.lower()}d."
        )

    # --------------------------------------------------
    # Report
    # --------------------------------------------------

    if result.get("report"):

        st.header(
            "📄 Research Report"
        )

        st.text_area(
            label="Final Report",
            value=result["report"],
            height=500
        )

    # --------------------------------------------------
    # PDF Download
    # --------------------------------------------------

    pdf_path = result.get(
        "pdf_path"
    )

    if (
        pdf_path
        and os.path.exists(pdf_path)
    ):

        st.header(
            "📥 Download PDF"
        )

        with open(
            pdf_path,
            "rb"
        ) as file:

            st.download_button(
                label="Download PDF Report",
                data=file,
                file_name=os.path.basename(
                    pdf_path
                ),
                mime="application/pdf"
            )


if __name__ == "__main__":
    main()