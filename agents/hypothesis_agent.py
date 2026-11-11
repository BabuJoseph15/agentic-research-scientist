"""
Hypothesis Agent.

Uses GPT-4o to generate scientific
reasoning and hypotheses based on:

- Research Question
- Literature Evidence
- Statistical Analysis

Author:
    Babu Guduru
"""

from services.llm_service import llm


def hypothesis_agent(state):
    """
    Generate a scientific hypothesis
    using GPT-4o.

    Args:
        state (dict):
            Current workflow state.

    Returns:
        dict:
            Updated workflow state.
    """

    prompt = f"""
You are a senior research scientist.

Research Question:
{state['question']}

Research Evidence:
{state['evidence']}

Statistical Findings:
{state['analysis']}

Your task:

1. Summarize findings.
2. Identify strongest climate factors.
3. Explain limitations.
4. Provide confidence level.
5. Generate a scientific hypothesis.

Use professional scientific writing.
"""

    response = llm.invoke(prompt)

    state["hypothesis"] = response.content

    return state