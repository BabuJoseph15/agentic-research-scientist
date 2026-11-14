"""
PDF Library.

Displays previously generated
PDF reports.

Author:
    Babu Guduru
"""

from pathlib import Path

import streamlit as st


REPORT_DIR = Path("reports")


def render_pdf_library():
    """
    Render PDF report library.
    """

    st.header(
        "📁 PDF Report Library"
    )

    pdf_files = sorted(
        REPORT_DIR.glob(
            "report_*.pdf"
        ),
        reverse=True
    )

    if not pdf_files:

        st.info(
            "No PDF reports found."
        )

        return

    for pdf_file in pdf_files:

        with open(
            pdf_file,
            "rb"
        ) as file:

            st.download_button(
                label=f"📄 {pdf_file.name}",
                data=file.read(),
                file_name=pdf_file.name,
                mime="application/pdf",
                key=f"pdf_{pdf_file.name}"
            )