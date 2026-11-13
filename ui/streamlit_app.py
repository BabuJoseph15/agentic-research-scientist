"""
Streamlit User Interface.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.0
"""

import os

import streamlit as st

from graph.workflow import graph

from agents.report_agent import report_agent


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


def run_workflow(question: str):

    state = initialize_state()

    state["question"] = question

    return graph.invoke(state)


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
Research workflow powered by:

- ArXiv Research Retrieval
- Statistical Analysis
- GPT-4o Reasoning
- Human Approval
- PDF Report Generation
"""
    )

    question = st.text_area(
        "Research Question",
        value=(
            "Can climate change increase "
            "dengue outbreaks in India?"
        ),
        height=120
    )

    if st.button(
        "🚀 Run Research Workflow"
    ):

        with st.spinner(

            "Generating scientific analysis..."
        ):

            result = run_workflow(
                question
            )

        st.session_state[
            "workflow_result"
        ] = result

    if "workflow_result" not in st.session_state:

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

    for paper in result["papers"]:

        with st.expander(
            paper["title"]
        ):

            st.write(
                f"Published: "
                f"{paper['published']}"
            )

            st.write(
                "Authors:"
            )

            for author in paper["authors"]:

                st.write(
                    f"- {author}"
                )

            st.write(
                f"URL: {paper['url']}"
            )

    # --------------------------------------------------
    # Statistics
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
        "🧠 GPT Scientific Assessment"
    )

    st.text_area(
        "",
        result["hypothesis"],
        height=450
    )

    # --------------------------------------------------
    # Approval
    # --------------------------------------------------

    st.header(
        "✅ Human Review"
    )

    review = st.radio(
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
            if review == "Approve"
            else "no"
        )

        result = report_agent(
            result
        )

        st.session_state[
            "workflow_result"
        ] = result

        st.success(
            f"Research {review.lower()}ed."
        )

    # --------------------------------------------------
    # Final Report
    # --------------------------------------------------

    if result.get("report"):

        st.header(
            "📄 Final Report"
        )

        st.text_area(
            "",
            value=result["report"],
            height=500
        )

    # --------------------------------------------------
    # PDF Download
    # --------------------------------------------------

    pdf_path = result.get(
        "pdf_path"
    )

    if pdf_path and os.path.exists(
        pdf_path
    ):

        st.header(
            "📥 Download PDF"
        )

        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name=os.path.basename(
                    pdf_path
                ),
                mime="application/pdf"
            )


if __name__ == "__main__":

    main()