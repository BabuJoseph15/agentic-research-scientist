from tools.dataset_tool import load_dataset
from tools.statistics_tool import correlation_analysis


def analysis_agent(state):

    df = load_dataset()

    correlations = correlation_analysis(df)

    state["analysis"] = correlations

    return state