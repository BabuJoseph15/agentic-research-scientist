def hypothesis_agent(state):

    correlations = state["analysis"]

    strongest_factor = max(
        correlations,
        key=correlations.get
    )

    hypothesis = f"""
Research Question:
{state['question']}

Scientific Findings:

Strongest Factor:
{strongest_factor}

Correlation:
{correlations[strongest_factor]}

Hypothesis:

Climate-related variables appear to be
associated with dengue outbreaks.

The strongest observed relationship
was detected for {strongest_factor}.

Based on the literature review and
statistical analysis, increasing
{strongest_factor} may contribute to
higher dengue incidence rates.
"""

    state["hypothesis"] = hypothesis

    return state