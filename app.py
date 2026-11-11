from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from graph.workflow import graph


def main():
    load_dotenv()

    question = input(
        "Research question [Can climate change increase dengue outbreaks in India?]: "
    ).strip() or "Can climate change increase dengue outbreaks in India?"

    initial_state = {
        "question": question,
        "papers": [],
        "evidence": [],
        "analysis": {},
        "hypothesis": "",
        "approval": "",
        "report": "",
    }

    result = graph.invoke(initial_state)
    print(result["report"])

    report_path = Path("reports") / (
        f"research_report_{datetime.now():%Y%m%d_%H%M%S}.md"
    )
    report_path.write_text(result["report"], encoding="utf-8")
    print(f"\nSaved report to {report_path}")


if __name__ == "__main__":
    main()