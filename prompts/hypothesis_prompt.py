"""
Hypothesis Prompt Builder.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.2
"""


def build_hypothesis_prompt(
    question: str,
    evidence: list,
    analysis: dict,
    similar_research: str
):
    """
    Build GPT prompt using:

    - Previous memory
    - Current literature
    - Statistical findings

    Args:
        question (str):
            Research question.

        evidence (list):
            Research evidence.

        analysis (dict):
            Statistical results.

        similar_research (str):
            Retrieved memory.

    Returns:
        str:
            Prompt text.
    """

    return f"""
You are a Senior Research Scientist.

Research Question
-----------------

{question}

Previous Similar Research
-------------------------

{similar_research}

Current Research Evidence
-------------------------

{evidence}

Statistical Findings
--------------------

{analysis}

Instructions

1. Review previous research memory.
2. Identify patterns from memory.
3. Review current evidence.
4. Analyze statistical findings.
5. Compare historical and current evidence.
6. Generate a scientific hypothesis.

Return ONLY the following sections:

Summary of Evidence

Statistical Interpretation

Key Risk Factors

Limitations

Confidence Level

Scientific Hypothesis

Future Research Recommendations
"""