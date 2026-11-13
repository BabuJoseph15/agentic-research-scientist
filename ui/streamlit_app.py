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

import os
import sys

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

from graph.ui_workflow import (
    ui_graph
)

from agents.report_agent import (
    report_agent
)


# --------------------------------------------------
# Session State Initialization
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


# --------------------------------------------------
# Workflow Execution
# --------------------------------------------------

def run_workflow(question: str):
    """
    Execute UI workflow.

    Args:
        question (str):
            Research question.

    Returns:
        dict:
            Workflow result.
    """

    state = initialize_state()

    state["question"] = question

    return ui_graph.invoke(state)


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
    # Question Input
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
    # Run Analysis
    # --------------------------------------------------

    if st.button(
        "🚀 Generate Research Analysis"
    ):

        with st.spinner(
            "Running Agentic Research Workflow..."
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
    # Wait Until Workflow Completes
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
    # Research Papers
    # --------------------------------------------------

    st.header(
        "📚 Research Papers"
    )

    for paper in result.get(
        "papers",
        []
    ):

        with st.expander(
            paper.get(
                "title",
                "Unknown Paper"
            )
        ):

            st.write(
                f"**Published:** "
                f"{paper.get('published', 'N/A')}"
            )

            authors = paper.get(
                "authors",
                []
            )

            if authors:

                st.write(
                    "**Authors:**"
                )

                st.write(
                    ", ".join(authors)
                )

            st.write(
                f"**URL:** "
                f"{paper.get('url', 'N/A')}"
            )

    # --------------------------------------------------
    # Statistical Analysis
    # --------------------------------------------------

    st.header(
        "📊 Statistical Findings"
    )

    st.json(
        result.get(
            "analysis",
            {}
        )
    )

    # --------------------------------------------------
    # GPT Output
    # --------------------------------------------------

    st.header(
        "🧠 GPT-4o Scientific Analysis"
    )

    st.text_area(
        label="Generated Hypothesis",
        value=result.get(
            "hypothesis",
            ""
        ),
        height=500
    )

    # --------------------------------------------------
    # Human Review
    # --------------------------------------------------

    st.header(
        "✅ Human Review"
    )

    approval = st.radio(
        "Review Decision",
        [
            "Approve",
            "Reject"
        ],
        horizontal=True
    )

    # --------------------------------------------------
    # Generate Report
    # --------------------------------------------------

    if st.button(
        "📄 Generate Final Report"
    ):

        result["approval"] = (
            "yes"
            if approval == "Approve"
            else "no"
        )

        updated_result = (
            report_agent(result)
        )

        st.session_state[
            "workflow_result"
        ] = updated_result

        st.success(
            f"Hypothesis "
            f"{approval.lower()}ed."
        )

    # --------------------------------------------------
    # Display Report
    # --------------------------------------------------

    result = st.session_state[
        "workflow_result"
    ]

    if result.get(
        "report"
    ):

        st.header(
            "📑 Final Research Report"
        )

        st.text_area(
            label="Report",
            value=result["report"],
            height=500
        )

    # --------------------------------------------------
    # PDF Download
    # --------------------------------------------------

    pdf_path = result.get(
        "pdf_path",
        ""
    )

    if (
        pdf_path
        and os.path.exists(pdf_path)
    ):

        st.header(
            "📥 Download PDF Report"
        )

        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name=os.path.basename(
                    pdf_path
                ),
                mime="application/pdf"
            )

        st.success(
            f"PDF Available: "
            f"{os.path.basename(pdf_path)}"
        )


if __name__ == "__main__":
    main()