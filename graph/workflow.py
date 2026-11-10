from langgraph.graph import StateGraph, END

from state.research_state import ResearchState

from agents.research_agent import research_agent
from agents.evidence_agent import evidence_agent
from agents.analysis_agent import analysis_agent
from agents.hypothesis_agent import hypothesis_agent


# Create workflow
workflow = StateGraph(ResearchState)

# Add nodes
workflow.add_node(
    "research",
    research_agent
)

workflow.add_node(
    "evidence",
    evidence_agent
)

workflow.add_node(
    "analysis",
    analysis_agent
)

workflow.add_node(
    "hypothesis",
    hypothesis_agent
)

# Entry point
workflow.set_entry_point(
    "research"
)

# Workflow edges
workflow.add_edge(
    "research",
    "evidence"
)

workflow.add_edge(
    "evidence",
    "analysis"
)

workflow.add_edge(
    "analysis",
    "hypothesis"
)

workflow.add_edge(
    "hypothesis",
    END
)

# Compile graph
graph = workflow.compile()