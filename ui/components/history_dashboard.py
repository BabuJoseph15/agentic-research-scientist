"""
Research History Dashboard.

Displays previous workflow runs.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.1
"""

import pandas as pd

import streamlit as st

from utils.cache_manager import (
    load_report_history
)


def render_history_dashboard():
    """
    Render research history dashboard.
    """

    history = load_report_history()

    st.header(
        "📜 Research History"
    )

    if not history:

        st.info(
            "No historical research records found."
        )

        return

    # --------------------------------------------------
    # Summary Metrics
    # --------------------------------------------------

    st.metric(
        "Total Research Runs",
        len(history)
    )

    # --------------------------------------------------
    # History Table
    # --------------------------------------------------

    rows = []

    for item in history:

        rows.append(
            {
                "Timestamp":
                item.get(
                    "timestamp",
                    "N/A"
                ),

                "Question":
                item.get(
                    "question",
                    "N/A"
                ),

                "Approval":
                item.get(
                    "approval",
                    "N/A"
                ).upper()
            }
        )

    df = pd.DataFrame(
        rows
    )

    st.dataframe(
        df,
        width="stretch"
    )

    # --------------------------------------------------
    # Latest Research Entry
    # --------------------------------------------------

    latest_entry = history[-1]

    st.subheader(
        "🧠 Latest Stored Hypothesis"
    )

    st.text_area(
        label="Latest Stored Hypothesis",
        value=latest_entry.get(
            "hypothesis",
            ""
        ),
        height=300,
        disabled=True
    )

    # --------------------------------------------------
    # Latest Research Question
    # --------------------------------------------------

    st.subheader(
        "❓ Latest Research Question"
    )

    st.info(
        latest_entry.get(
            "question",
            "N/A"
        )
    )