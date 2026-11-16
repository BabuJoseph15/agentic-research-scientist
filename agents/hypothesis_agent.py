"""
Hypothesis Agent.

Generates scientific hypotheses
using GPT-4o.

Enhanced with ChromaDB memory retrieval.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.2
"""

from services.llm_service import llm

from prompts.hypothesis_prompt import (
    build_hypothesis_prompt
)

from memory.chroma_manager import (
    retrieve_similar_research
)

from utils.logger import logger


def hypothesis_agent(state):
    """
    Generate scientific hypothesis.

    Args:
        state (dict):
            Workflow state.

    Returns:
        dict:
            Updated workflow state.
    """

    logger.info(
        "Hypothesis Agent Started"
    )

    try:

        # ------------------------------------------
        # Retrieve Memory
        # ------------------------------------------

        memory_results = (
            retrieve_similar_research(
                state["question"],
                top_k=3
            )
        )

        memory_context = (
            "No previous research found."
        )

        if (
            memory_results
            and
            "documents" in memory_results
            and
            memory_results["documents"]
        ):

            documents = (
                memory_results[
                    "documents"
                ][0]
            )

            if documents:

                logger.info(
                    f"Retrieved "
                    f"{len(documents)} "
                    f"similar research documents."
                )

                memory_sections = []

                for idx, document in enumerate(
                    documents,
                    start=1
                ):

                    memory_sections.append(
                        f"""
Research {idx}

{document[:1500]}
"""
                    )

                memory_context = (
                    "\n".join(
                        memory_sections
                    )
                )

        # ------------------------------------------
        # Build Prompt
        # ------------------------------------------

        prompt = (
            build_hypothesis_prompt(
                question=
                state["question"],

                evidence=
                state["evidence"],

                analysis=
                state["analysis"],

                similar_research=
                memory_context
            )
        )

        # ------------------------------------------
        # GPT Invocation
        # ------------------------------------------

        response = (
            llm.invoke(prompt)
        )

        state["hypothesis"] = (
            response.content
        )

        logger.info(
            "Hypothesis generated."
        )

    except Exception as ex:

        logger.error(
            f"Hypothesis error: {ex}"
        )

        state["hypothesis"] = (
            f"Unable to generate "
            f"hypothesis: {str(ex)}"
        )

    return state