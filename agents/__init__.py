"""
Agents Module
=============

LangChain-based agents for the AgenticAI Foundry.

This module contains single-agent implementations that use tools,
contrasting with the multi-agent CrewAI approach in the crews/ module.

Available agents:
- crypto_agent: Web search agent for cryptocurrency prices
"""

from .crypto_agent import run_crypto_agent, AgentResult, AgentTelemetry

__all__ = ["run_crypto_agent", "AgentResult", "AgentTelemetry"]
