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
          END

Responsibilities:

1. Define all workflow nodes.
2. Define transitions between agents.
3. Define workflow entry point.
4. Compile the LangGraph execution graph.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    0.1
"""

from langgraph.graph import StateGraph, END

from state.research_state import ResearchState

from agents.research_agent import research_agent
from agents.evidence_agent import evidence_agent
from agents.analysis_agent import analysis_agent
from agents.hypothesis_agent import hypothesis_agent


# ------------------------------------------------------------------
# Create Workflow
# ------------------------------------------------------------------
"""
Create a LangGraph workflow instance using the
shared ResearchState object.

The state object acts as a central memory
container passed between all agents.
"""
workflow = StateGraph(ResearchState)


# ------------------------------------------------------------------
# Register Nodes
# ------------------------------------------------------------------
"""
Register all agents as LangGraph nodes.

Each node receives the current workflow state,
performs its assigned task, and returns the
updated state.
"""

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


# ------------------------------------------------------------------
# Define Entry Point
# ------------------------------------------------------------------
"""
The Research Agent serves as the workflow
entry point.

Execution begins here whenever the graph
is invoked.
"""

workflow.set_entry_point(
    "research"
)


# ------------------------------------------------------------------
# Define Workflow Edges
# ------------------------------------------------------------------
"""
Define execution order between agents.

State Flow:

Question
    ↓
Research Agent
    ↓
Evidence Agent
    ↓
Analysis Agent
    ↓
Hypothesis Agent
    ↓
END
"""

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


# ------------------------------------------------------------------
# Compile Workflow
# ------------------------------------------------------------------
"""
Compile the workflow into an executable graph.

The compiled graph can be invoked from:

    app.py

Example:

    result = graph.invoke(initial_state)
"""

graph = workflow.compile()