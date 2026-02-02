"""
CrewAI Multi-Agent Demos
MIT Professional Education: Agentic AI

This package contains standalone crew definitions that can be run via CLI
or imported into Streamlit apps.
"""

from .research_crew import (
    run_research_crew,
    get_available_providers,
    check_ollama_running,
    check_ollama_model,
    PROVIDER_CONFIGS,
    CrewResult
)

__all__ = [
    "run_research_crew",
    "get_available_providers", 
    "check_ollama_running",
    "check_ollama_model",
    "PROVIDER_CONFIGS",
    "CrewResult"
]
