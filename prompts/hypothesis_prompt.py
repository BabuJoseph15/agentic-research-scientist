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
    0.6
"""


def build_hypothesis_prompt(
    question: str,
    evidence: list,
    analysis: dict
) -> str:
    """
    Build GPT-4o hypothesis generation prompt.

    Args:
        question (str):
            Research question.

        evidence (list):
            Extracted evidence.

        analysis (dict):
            Statistical findings.

    Returns:
        str:
            Formatted prompt.
    """

    return f"""
You are a Senior Research Scientist specializing in:

- Epidemiology
- Climate Science
- Public Health
- Data Analysis

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

Analyze the research evidence and statistical findings.

Return your response using only the sections below.

Do not use markdown symbols such as:
**, #, -, or bullet formatting.

Use plain text.

Required Sections:

Summary of Evidence

Statistical Interpretation

Key Risk Factors

Limitations

Confidence Level

Scientific Hypothesis

Future Research Recommendations

Keep the writing concise, scientific,
and suitable for an executive report.
"""