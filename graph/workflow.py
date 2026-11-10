from langgraph.graph import StateGraph
from langgraph.graph import END

from state.research_state import ResearchState

from agents.research_agent import research_agent
from agents.evidence_agent import evidence_agent

workflow = StateGraph(
    ResearchState
)

workflow.add_node(
    "research",
    research_agent
)

workflow.add_node(
    "evidence",
    evidence_agent
)

workflow.set_entry_point(
    "research"
)

workflow.add_edge(
    "research",
    "evidence"
)

workflow.add_edge(
    "evidence",
    END
)

graph = workflow.compile()