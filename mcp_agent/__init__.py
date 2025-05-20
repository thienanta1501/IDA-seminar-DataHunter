"""MCP Agent for AI-Driven Data Application.

This package provides an agent implementation for the AI-Driven Data Application
with a 3-part architecture. The agent uses LangGraph to analyze user input,
design multi-step workflows, and call appropriate tools on the MCP Server.
"""

from mcp_agent.agent_gemini import DataAgentGraph

__all__ = ["DataAgentGraph"] 