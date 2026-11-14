"""
Agentic Research Scientist.

Streamlit Application.

Features:

1. Research Analysis
2. ChromaDB Memory Retrieval
3. GPT-4o Scientific Reasoning
4. Human Review
5. PDF Report Generation
6. Research History Dashboard
7. PDF Library

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
# Application Imports
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
# Workflow State
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
            label="Enter Research Question",
            value=(
                "Can climate change increase "
                "dengue outbreaks in India?"
            ),
            height=120
        )

        # ----------------------------------------------
        # Memory Statistics
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
        # Similar Memory Preview
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
                and
                len(
                    memory_results[
                        "documents"
                    ]
                ) > 0
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

        if (
            "workflow_result"
            not in st.session_state
        ):
            return

        result = st.session_state[
            "workflow_result"
        ]

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
        # Statistics
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

        if st.button(
            "📄 Generate Final Report"
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

            st.success(
                f"Hypothesis "
                f"{review_decision.lower()}d."
            )

            st.rerun()

        # ----------------------------------------------
        # Refresh Session State
        # ----------------------------------------------

        result = st.session_state[
            "workflow_result"
        ]

        # ----------------------------------------------
        # Final Report
        # ----------------------------------------------

        if result.get(
            "report"
        ):

            st.header(
                "📑 Final Research Report"
            )

            st.text_area(
                label="Generated Report",
                value=result[
                    "report"
                ],
                height=500
            )

        # ----------------------------------------------
        # Download Latest PDF
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
            ) as file:

                st.download_button(
                    label=
                    "Download Latest PDF",

                    data=
                    file.read(),

                    file_name=
                    os.path.basename(
                        pdf_path
                    ),

                    mime=
                    "application/pdf"
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
# Entrypoint
# --------------------------------------------------

if __name__ == "__main__":

    main()