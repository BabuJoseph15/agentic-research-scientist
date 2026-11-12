"""
Hypothesis Agent.

Uses GPT-4o to generate scientific
reasoning and research hypotheses.

Inputs:

- Research Question
- Research Evidence
- Statistical Findings

Outputs:

- Scientific Findings
- Risk Factors
- Limitations
- Confidence Assessment
- Scientific Hypothesis

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.5
"""

from services.llm_service import (
    llm
)

from prompts.hypothesis_prompt import (
    build_hypothesis_prompt
)

from utils.logger import logger


def hypothesis_agent(state):
    """
    Generate a scientific hypothesis using GPT-4o.

    Args:
        state (dict):
            Current LangGraph workflow state.

    Returns:
        dict:
            Updated workflow state containing
            GPT-generated hypothesis.
    """

    logger.info(
        "Hypothesis Agent Started"
    )

    try:

        prompt = (
            build_hypothesis_prompt(
                question=
                state["question"],

                evidence=
                state["evidence"],

                analysis=
                state["analysis"]
            )
        )

        response = (
            llm.invoke(prompt)
        )

        state["hypothesis"] = (
            response.content
        )

        logger.info(
            "Hypothesis successfully generated"
        )

    except Exception as ex:

        logger.error(
            f"Hypothesis generation failed: "
            f"{str(ex)}"
        )

        state["hypothesis"] = (
            "Unable to generate "
            "scientific hypothesis."
        )

    return state