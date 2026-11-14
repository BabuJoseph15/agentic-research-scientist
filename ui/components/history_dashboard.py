"""
Research History Dashboard.

Displays previous workflow runs.

Author:
    Babu Guduru
"""

import pandas as pd

import streamlit as st

from utils.cache_manager import (
    load_report_history
)


def render_history_dashboard():
    """
    Render history page.
    """

    history = (
        load_report_history()
    )

    if not history:

        st.info(
            "No historical records found."
        )

        return

    st.header(
        "📜 Research History"
    )

    rows = []

    for item in history:

        rows.append(
            {
                "Timestamp":
                item.get(
                    "timestamp"
                ),

                "Question":
                item.get(
                    "question"
                ),

                "Approval":
                item.get(
                    "approval"
                )
            }
        )

    df = pd.DataFrame(
        rows
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader(
        "Latest Hypothesis"
    )

    st.text_area(
        "",
        value=history[-1].get(
            "hypothesis",
            ""
        ),
        height=250
    )