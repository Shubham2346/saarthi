"""
Saarthi Multi-Agent System — LangGraph Orchestration

This package implements the agentic layer:
- Supervisor/Router: classifies student intent and routes to the right agent
- FAQ Agent: answers knowledge-base questions via RAG
- Task Agent: manages onboarding checklist from the database
- Escalation Agent: creates support tickets for unresolved queries

The agents are wired together as a LangGraph StateGraph.
"""

from app.agents.graph import create_agent_graph, run_agent

__all__ = ["create_agent_graph", "run_agent"]
