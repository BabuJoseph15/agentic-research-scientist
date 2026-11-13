"""
UI Workflow.

Streamlit-specific workflow that generates:

- Research Papers
- Evidence
- Statistical Analysis
- GPT Hypothesis

Human approval and report generation are
handled directly in the Streamlit interface.

Author:
    Babu Guduru

Project:
    Agentic Research Scientist

Version:
    1.0
"""

from langgraph.graph import StateGraph
from langgraph.graph import END

from state.research_state import (
    ResearchState
)

from agents.research_agent import (
    research_agent
)

from agents.evidence_agent import (
    evidence_agent
)

from agents.analysis_agent import (
    analysis_agent
)

from agents.hypothesis_agent import (
    hypothesis_agent
)


# --------------------------------------------------
# Build Workflow
# --------------------------------------------------

workflow = StateGraph(
    ResearchState
)

# --------------------------------------------------
# Nodes
# --------------------------------------------------

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

# --------------------------------------------------
# Flow
# --------------------------------------------------

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

#
# Stop here for Streamlit
#
workflow.add_edge(
    "hypothesis",
    END
)

# --------------------------------------------------
# Compile
# --------------------------------------------------

ui_graph = workflow.compile()