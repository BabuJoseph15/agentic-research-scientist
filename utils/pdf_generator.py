"""
PDF Generator.

Responsible for generating PDF reports
for completed research workflow executions.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.7
"""

from pathlib import Path

from datetime import datetime

from reportlab.lib.pagesizes import letter

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from utils.logger import logger


REPORTS_DIR = (
    Path(__file__).parent.parent
    / "reports"
)

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def generate_pdf_report(
    question: str,
    report: str
) -> str:
    """
    Generate research report PDF.

    Args:
        question (str):
            Original research question.

        report (str):
            Final generated report.

    Returns:
        str:
            Generated PDF file path.
    """

    try:

        timestamp = (
            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
        )

        pdf_file = (
            REPORTS_DIR
            / f"report_{timestamp}.pdf"
        )

        document = SimpleDocTemplate(
            str(pdf_file),
            pagesize=letter
        )

        styles = (
            getSampleStyleSheet()
        )

        story = []

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Agentic Research Scientist",
                styles["Title"]
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # --------------------------------------------------
        # Timestamp
        # --------------------------------------------------

        story.append(
            Paragraph(
                f"Generated: "
                f"{datetime.now()}",
                styles["Normal"]
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # --------------------------------------------------
        # Research Question
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Research Question",
                styles["Heading1"]
            )
        )

        story.append(
            Paragraph(
                question,
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # --------------------------------------------------
        # Report Content
        # --------------------------------------------------

        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                "Research Report",
                styles["Heading1"]
            )
        )

        # Convert line breaks for PDF rendering
        formatted_report = (
            report.replace(
                "\n",
                "<br/>"
            )
        )

        story.append(
            Paragraph(
                formatted_report,
                styles["BodyText"]
            )
        )

        document.build(
            story
        )

        logger.info(
            f"PDF created: {pdf_file}"
        )

        print(
            f"\n✅ PDF Report Generated: "
            f"{pdf_file}"
        )

        return str(pdf_file)

    except Exception as ex:

        logger.error(
            f"PDF generation failed: "
            f"{str(ex)}"
        )

        return ""