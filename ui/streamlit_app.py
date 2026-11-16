"""
Agentic Research Scientist.

Streamlit Application.

Author:
    Babu Guduru

Version:
    1.2
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

    sys.path.append(
        str(PROJECT_ROOT)
    )


# --------------------------------------------------
# Imports
# --------------------------------------------------

from graph.ui_workflow import (
    ui_graph
)

from agents.report_agent import (
    report_agent
)

from memory.chroma_manager import (
    memory_count,
    retrieve_similar_research
)

from ui.components.history_dashboard import (
    render_history_dashboard
)

from ui.components.pdf_library import (
    render_pdf_library
)


# --------------------------------------------------
# State Helpers
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


def run_workflow(
    question: str
):

    state = initialize_state()

    state["question"] = question

    return ui_graph.invoke(
        state
    )


# --------------------------------------------------
# Main
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

    # --------------------------------------------------
    # Session State
    # --------------------------------------------------

    if (
        "report_generated"
        not in st.session_state
    ):

        st.session_state[
            "report_generated"
        ] = False

    if (
        "workflow_result"
        not in st.session_state
    ):

        st.session_state[
            "workflow_result"
        ] = None

    st.markdown(
        """
Generate research insights using:

- ArXiv Retrieval
- Statistical Analysis
- GPT-4o Scientific Reasoning
- ChromaDB Memory
- Human Review
- PDF Reports
"""
    )

    # --------------------------------------------------
    # Tabs
    # --------------------------------------------------

    research_tab, history_tab, reports_tab = (
        st.tabs(
            [
                "🔬 Research",
                "📜 History",
                "📁 Reports"
            ]
        )
    )

    # ==================================================
    # RESEARCH TAB
    # ==================================================

    with research_tab:

        st.header(
            "Research Question"
        )

        question = st.text_area(
            label=
            "Enter Research Question",

            value=(
                "Can climate change increase "
                "dengue outbreaks in India?"
            ),

            height=120
        )

        # ----------------------------------------------
        # Memory Stats
        # ----------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Stored Research Memories",
                memory_count()
            )

        with col2:

            st.metric(
                "Memory Retrieval",
                "Enabled"
            )

        # ----------------------------------------------
        # Similar Research
        # ----------------------------------------------

        if question:

            memory_results = (
                retrieve_similar_research(
                    question,
                    top_k=3
                )
            )

            if (
                memory_results
                and
                "documents"
                in memory_results
            ):

                docs = (
                    memory_results[
                        "documents"
                    ][0]
                )

                if docs:

                    st.subheader(
                        "🧠 Similar Research Memory"
                    )

                    for idx, doc in enumerate(
                        docs,
                        start=1
                    ):

                        with st.expander(
                            f"Memory Match {idx}"
                        ):

                            st.write(
                                doc[:2000]
                            )

        # ----------------------------------------------
        # Generate Analysis
        # ----------------------------------------------

        if st.button(
            "🚀 Generate Research Analysis",
            type="primary"
        ):

            st.session_state[
                "report_generated"
            ] = False

            with st.spinner(
                "Running research workflow..."
            ):

                result = (
                    run_workflow(
                        question
                    )
                )

            st.session_state[
                "workflow_result"
            ] = result

            st.success(
                "Research analysis completed."
            )

        result = st.session_state.get(
            "workflow_result"
        )

        if not result:

            return

        # ----------------------------------------------
        # Research Papers
        # ----------------------------------------------

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
                    "title",
                    "Unknown Paper"
                )
            ):

                st.write(
                    f"**Published:** "
                    f"{paper.get('published', 'N/A')}"
                )

                st.write(
                    f"**Authors:** "
                    f"{', '.join(paper.get('authors', []))}"
                )

                st.write(
                    f"**URL:** "
                    f"{paper.get('url', 'N/A')}"
                )

        # ----------------------------------------------
        # Analysis
        # ----------------------------------------------

        st.header(
            "📊 Statistical Findings"
        )

        st.json(
            result.get(
                "analysis",
                {}
            )
        )

        # ----------------------------------------------
        # GPT Analysis
        # ----------------------------------------------

        st.header(
            "🧠 GPT-4o Scientific Analysis"
        )

        st.markdown(
            result.get(
                "hypothesis",
                ""
            )
        )

        # ----------------------------------------------
        # Human Review
        # ----------------------------------------------

        st.header(
            "✅ Human Review"
        )

        review_decision = (
            st.radio(
                "Review Decision",
                [
                    "Approve",
                    "Reject"
                ],
                horizontal=True
            )
        )

        # ----------------------------------------------
        # Generate Report
        # ----------------------------------------------

        if (
            st.button(
                "📄 Generate Final Report"
            )
            and
            not st.session_state[
                "report_generated"
            ]
        ):

            result["approval"] = (
                "yes"
                if review_decision
                == "Approve"
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

            st.session_state[
                "report_generated"
            ] = True

            st.success(
                f"Hypothesis "
                f"{review_decision.lower()}d."
            )

            st.rerun()

        # ----------------------------------------------
        # Refresh Result
        # ----------------------------------------------

        result = st.session_state.get(
            "workflow_result"
        )

        # ----------------------------------------------
        # Final Report
        # ----------------------------------------------

        if result.get(
            "report"
        ):

            st.header(
                "📑 Final Research Report"
            )

            st.code(
                result["report"],
                language="text"
            )

        # ----------------------------------------------
        # Latest PDF
        # ----------------------------------------------

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
                    "application/pdf",

                    key=
                    "latest_pdf"
                )

    # ==================================================
    # HISTORY TAB
    # ==================================================

    with history_tab:

        render_history_dashboard()

    # ==================================================
    # REPORTS TAB
    # ==================================================

    with reports_tab:

        render_pdf_library()


# --------------------------------------------------
# Entry
# --------------------------------------------------

if __name__ == "__main__":

    main()