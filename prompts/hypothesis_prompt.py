"""
Hypothesis Prompt Builder.

Contains reusable prompt templates used by the
Hypothesis Agent for generating scientific
reasoning and hypotheses.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.5
"""


def build_hypothesis_prompt(
    question: str,
    evidence: list,
    analysis: dict
) -> str:
    """
    Build hypothesis generation prompt.

    Args:
        question (str):
            Research question.

        evidence (list):
            Extracted evidence from papers.

        analysis (dict):
            Statistical findings.

    Returns:
        str:
            Fully formatted prompt for GPT-4o.
    """

    return f"""
You are a Senior Research Scientist specializing
in Epidemiology, Climate Science and Public Health.

Research Question:
------------------
{question}

Research Evidence:
------------------
{evidence}

Statistical Findings:
------------------
{analysis}

Instructions:
-------------

1. Summarize available evidence.
2. Interpret statistical findings.
3. Identify key risk factors.
4. Explain limitations.
5. Provide confidence assessment:
    - Low
    - Medium
    - High
6. Generate a scientific hypothesis.
7. Suggest future research directions.

Respond using the following structure:

Summary of Evidence

Statistical Interpretation

Key Risk Factors

Limitations

Confidence Level

Scientific Hypothesis

Future Research Recommendations
"""