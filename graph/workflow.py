"""
LangGraph Workflow Definition.

This module defines the orchestration layer of the
Agentic Research Scientist application.

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
    Report Agent
          ↓
          END

Responsibilities:

1. Register workflow agents.
2. Define execution order.
3. Define workflow entry point.
4. Compile executable LangGraph workflow.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.2
"""

from langgraph.graph import StateGraph, END

from state.research_state import ResearchState

from agents.research_agent import research_agent
from agents.evidence_agent import evidence_agent
from agents.analysis_agent import analysis_agent
from agents.hypothesis_agent import hypothesis_agent
from agents.approval_agent import approval_agent
from agents.report_agent import report_agent


# ------------------------------------------------------------------
# Workflow Initialization
# ------------------------------------------------------------------

workflow = StateGraph(ResearchState)


# ------------------------------------------------------------------
# Register Workflow Nodes
# ------------------------------------------------------------------

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

workflow.add_node(
    "report",
    report_agent
)


# ------------------------------------------------------------------
# Set Workflow Entry Point
# ------------------------------------------------------------------

workflow.set_entry_point(
    "research"
)


# ------------------------------------------------------------------
# Workflow Execution Path
# ------------------------------------------------------------------

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
    "report"
)

workflow.add_edge(
    "report",
    END
)


# ------------------------------------------------------------------
# Compile Workflow
# ------------------------------------------------------------------

graph = workflow.compile()