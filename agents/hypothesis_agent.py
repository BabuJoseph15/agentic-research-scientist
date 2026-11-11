"""
Hypothesis Agent.

Uses GPT-4o to generate scientific reasoning
and research hypotheses based on:

- Research Question
- Scientific Evidence
- Statistical Findings

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.4
"""

from services.llm_service import llm

from utils.logger import logger


def hypothesis_agent(state):
    """
    Generate a scientific hypothesis using GPT-4o.

    Args:
        state (dict):
            Current workflow state.

    Returns:
        dict:
            Updated workflow state containing
            the generated hypothesis.
    """

    logger.info(
        "Hypothesis Agent Started"
    )

    prompt = f"""
You are a senior epidemiologist and climate researcher.

Research Question:
{state['question']}

Research Evidence:
{state['evidence']}

Statistical Findings:
{state['analysis']}

Instructions:

1. Summarize the evidence.
2. Interpret the statistical findings.
3. Identify the strongest risk factors.
4. Mention limitations.
5. Provide a confidence assessment.
6. Generate a scientific hypothesis.

Use professional scientific language.
"""

    response = llm.invoke(prompt)

    state["hypothesis"] = response.content

    logger.info(
        "Hypothesis successfully generated"
    )

    return state