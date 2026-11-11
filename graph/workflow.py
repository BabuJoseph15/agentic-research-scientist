"""
LangGraph Workflow Definition.

Workflow:

    Research Agent
          ↓
    Evidence Agent
          ↓
    Analysis Agent
          ↓
    Hypothesis Agent
          ↓
    Approval Agent
          ↓
          END

Author:
    Babu Guduru
"""

from langgraph.graph import StateGraph, END

from state.research_state import ResearchState

from agents.research_agent import research_agent
from agents.evidence_agent import evidence_agent
from agents.analysis_agent import analysis_agent
from agents.hypothesis_agent import hypothesis_agent
from agents.approval_agent import approval_agent
from agents.report_agent import report_agent


workflow = StateGraph(ResearchState)


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

workflow.add_node(
    "approval",
    approval_agent
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
    "analysis"
)

workflow.add_edge(
    "analysis",
    "hypothesis"
)

workflow.add_edge(
    "hypothesis",
    "approval"
)

workflow.add_edge(
    "approval",
    END
)


graph = workflow.compile()