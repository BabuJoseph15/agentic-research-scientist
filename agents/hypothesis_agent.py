"""
Hypothesis Agent.

Generates scientific hypotheses
using GPT-4o.

Enhanced with ChromaDB memory.

Author:
    Babu Guduru
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

    logger.info(
        "Hypothesis Agent Started"
    )

    try:

        # ------------------------------------
        # Memory Retrieval
        # ------------------------------------

        memory_results = (
            retrieve_similar_research(
                state["question"]
            )
        )

        memory_context = ""

        if (
            memory_results
            and
            "documents"
            in memory_results
            and
            len(
                memory_results["documents"]
            ) > 0
        ):

            documents = (
                memory_results[
                    "documents"
                ][0]
            )

            for idx, document in enumerate(
                documents,
                start=1
            ):

                memory_context += (
                    f"\nResearch {idx}\n"
                    f"{document[:1000]}\n"
                )

        else:

            memory_context = (
                "No similar research found."
            )

        # ------------------------------------
        # Prompt
        # ------------------------------------

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
            "Unable to generate "
            "hypothesis."
        )

    return state