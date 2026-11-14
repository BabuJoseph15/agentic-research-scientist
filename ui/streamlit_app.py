"""
Streamlit User Interface.

Agentic Research Scientist.

Author:
    Babu Guduru

Version:
    1.1
"""

import os
import sys

from pathlib import Path

import streamlit as st


# --------------------------------------------------
# Path Setup
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(
        str(PROJECT_ROOT)
    )


# --------------------------------------------------
# Workflow Imports
# --------------------------------------------------

from graph.ui_workflow import (
    ui_graph
)

from agents.report_agent import (
    report_agent
)

from ui.components.history_dashboard import (
    render_history_dashboard
)

from ui.components.pdf_library import (
    render_pdf_library
)


# --------------------------------------------------
# Initial State
# --------------------------------------------------

def initialize_state():

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

def run_workflow(
    question: str
):

    state = initialize_state()

    state["question"] = question

    return ui_graph.invoke(
        state
    )


# --------------------------------------------------
# Main Application
# --------------------------------------------------

def main():

    st.set_page_config(
        page_title=
        "Agentic Research Scientist",

        page_icon="🔬",

        layout="wide"
    )

    st.title(
        "🔬 Agentic Research Scientist"
    )

    st.markdown(
        """
Generate research insights using:

- ArXiv Retrieval
- Statistical Analysis
- GPT-4o Scientific Reasoning
- Human Review
- PDF Reports
- ChromaDB Memory
"""
    )

    st.divider()

    # --------------------------------------------------
    # Research Question
    # --------------------------------------------------

    question = st.text_area(
        "Research Question",

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
        "🚀 Generate Research Analysis",

        type="primary"
    ):

        with st.spinner(
            "Running workflow..."
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
    # Wait
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

    st.caption(
        f"{len(result.get('papers', []))} "
        f"papers retrieved"
    )

    for paper in result.get(
        "papers",
        []
    ):

        with st.expander(
            paper.get(
                "title"
            )
        ):

            st.write(
                f"**Published:** "
                f"{paper.get('published')}"
            )

            st.write(
                f"**Authors:** "
                f"{', '.join(paper.get('authors', []))}"
            )

            st.write(
                f"**URL:** "
                f"{paper.get('url')}"
            )

    # --------------------------------------------------
    # Analysis
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
    # GPT Analysis
    # --------------------------------------------------

    st.header(
        "🧠 GPT-4o Scientific Analysis"
    )

    st.markdown(
        result.get(
            "hypothesis",
            ""
        )
    )

    st.divider()

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

    if st.button(
        "📄 Generate Final Report"
    ):

        result["approval"] = (
            "yes"
            if approval == "Approve"
            else "no"
        )

        updated_result = (
            report_agent(
                result
            )
        )

        st.session_state[
            "workflow_result"
        ] = updated_result

        st.success(
            f"Hypothesis "
            f"{approval.lower()}d."
        )

        st.rerun()

    # --------------------------------------------------
    # Refresh state
    # --------------------------------------------------

    result = st.session_state[
        "workflow_result"
    ]

    # --------------------------------------------------
    # Final Report
    # --------------------------------------------------

    if result.get(
        "report"
    ):

        st.divider()

        st.header(
            "📑 Final Research Report"
        )

        st.text_area(
            "Report",

            value=result["report"],

            height=500
        )

    # --------------------------------------------------
    # Latest PDF
    # --------------------------------------------------

    pdf_path = result.get(
        "pdf_path",
        ""
    )

    if (
        pdf_path
        and
        os.path.exists(
            pdf_path
        )
    ):

        st.divider()

        st.header(
            "📥 Download Latest PDF"
        )

        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            st.download_button(
                label=
                "Download Latest PDF",

                data=
                pdf_file.read(),

                file_name=
                os.path.basename(
                    pdf_path
                ),

                mime=
                "application/pdf"
            )

    # --------------------------------------------------
    # History Dashboard
    # --------------------------------------------------

    st.divider()

    render_history_dashboard()

    # --------------------------------------------------
    # PDF Library
    # --------------------------------------------------

    st.divider()

    render_pdf_library()


if __name__ == "__main__":

    main()