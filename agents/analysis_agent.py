"""
Analysis Agent.

Performs statistical analysis on the
dengue dataset and produces correlation
metrics required for scientific reasoning.

Author: Babu Guduru
"""

from tools.dataset_tool import (
    load_dataset
)

from tools.statistics_tool import (
    correlation_analysis
)


def analysis_agent(state):
    """
    Execute dataframe analysis.

    Args:
        state (dict):
            Current LangGraph state.

    Returns:
        dict:
            Updated workflow state containing
            analytical findings.
    """

    df = load_dataset()

    correlations = (
        correlation_analysis(df)
    )

    state["analysis"] = correlations

    return state