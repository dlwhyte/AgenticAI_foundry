from __future__ import annotations
"""
CrewAI Research Team - Multi-Agent Demo
MIT Professional Education: Agentic AI

This module can be run standalone (CLI) or imported by Streamlit.

Usage (CLI):
    python -m crews.research_crew --provider ollama --task "Research AI in healthcare"
    python -m crews.research_crew --provider openai --task "Research AI in healthcare"

Usage (Import):
    from crews.research_crew import run_research_crew, get_available_providers
    result = run_research_crew("Research AI in healthcare", provider="ollama")
"""

import os
import sys
import argparse
from typing import Optional, Generator, Dict, Any
from dataclasses import dataclass
from enum import Enum

# CrewAI imports
try:
    from crewai import Agent, Task, Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

# LLM provider imports
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langchain_community.llms import Ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# =============================================================================
# CONFIGURATION
# =============================================================================

class Provider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"


@dataclass
class ProviderConfig:
    """Configuration for an LLM provider"""
    name: str
    display_name: str
    model: str
    requires_api_key: bool
    api_key_env: Optional[str]
    base_url: Optional[str]
    cost_per_1k_tokens: float  # Approximate cost for display
    description: str


# Provider configurations
PROVIDER_CONFIGS: Dict[str, ProviderConfig] = {
    "ollama": ProviderConfig(
        name="ollama",
        display_name="🏠 Ollama (Local)",
        model="llama3.2",  # Default model, can be changed
        requires_api_key=False,
        api_key_env=None,
        base_url="http://localhost:11434",
        cost_per_1k_tokens=0.0,
        description="Free, runs locally. Requires Ollama installed."
    ),
    "openai": ProviderConfig(
        name="openai",
        display_name="☁️ OpenAI",
        model="gpt-4o-mini",  # Cost-effective default
        requires_api_key=True,
        api_key_env="OPENAI_API_KEY",
        base_url=None,
        cost_per_1k_tokens=0.00015,  # $0.15 per 1M input
        description="Fast, high quality. Requires API key (~$0.01/run)."
    )
}


# =============================================================================
# LLM FACTORY
# =============================================================================

def get_llm(provider: str, api_key: Optional[str] = None, model: Optional[str] = None):
    """
    Create an LLM instance based on provider selection.
    
    Args:
        provider: "ollama" or "openai"
        api_key: API key (required for OpenAI, ignored for Ollama)
        model: Override default model
        
    Returns:
        LLM instance compatible with CrewAI
    """
    config = PROVIDER_CONFIGS.get(provider)
    if not config:
        raise ValueError(f"Unknown provider: {provider}. Choose from: {list(PROVIDER_CONFIGS.keys())}")
    
    model_name = model or config.model
    
    if provider == "ollama":
        if not OLLAMA_AVAILABLE:
            raise ImportError("langchain-community not installed. Run: pip install langchain-community")
        return Ollama(
            model=model_name,
            base_url=config.base_url
        )
    
    elif provider == "openai":
        if not OPENAI_AVAILABLE:
            raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")
        
        # Get API key from parameter, env, or raise error
        key = api_key or os.getenv(config.api_key_env)
        if not key:
            raise ValueError(f"OpenAI API key required. Set {config.api_key_env} or pass api_key parameter.")
        
        return ChatOpenAI(
            model=model_name,
            api_key=key,
            temperature=0.7
        )
    
    else:
        raise ValueError(f"Provider {provider} not implemented")


def get_available_providers() -> Dict[str, ProviderConfig]:
    """Return configs for providers that are installed and available."""
    available = {}
    
    if OLLAMA_AVAILABLE:
        available["ollama"] = PROVIDER_CONFIGS["ollama"]
    
    if OPENAI_AVAILABLE:
        available["openai"] = PROVIDER_CONFIGS["openai"]
    
    return available


def check_ollama_running() -> bool:
    """Check if Ollama is running locally."""
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except:
        return False


def check_ollama_model(model: str = "llama3.2") -> bool:
    """Check if a specific model is available in Ollama."""
    try:
        import urllib.request
        import json
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            models = [m.get("name", "").split(":")[0] for m in data.get("models", [])]
            return model in models
    except:
        return False


# =============================================================================
# AGENT DEFINITIONS
# =============================================================================

def create_research_crew(llm, verbose: bool = True) -> "Crew":
    """
    Create a research crew with three specialized agents.
    
    The crew follows a sequential process:
    1. Researcher gathers information
    2. Writer creates content from research
    3. Editor polishes and verifies
    
    Args:
        llm: Language model instance
        verbose: Whether to print agent activity
        
    Returns:
        Configured Crew instance
    """
    
    # Agent 1: Researcher
    researcher = Agent(
        role="Research Analyst",
        goal="Gather comprehensive, accurate information on the given topic",
        backstory="""You are an experienced research analyst with expertise in 
        finding and synthesizing information from multiple sources. You focus on 
        facts, statistics, and key insights that provide real value.""",
        llm=llm,
        verbose=verbose,
        allow_delegation=False
    )
    
    # Agent 2: Writer
    writer = Agent(
        role="Content Writer",
        goal="Transform research into clear, engaging, well-structured content",
        backstory="""You are a skilled content writer who excels at taking 
        complex information and making it accessible to a general audience. 
        You write in a professional but engaging tone.""",
        llm=llm,
        verbose=verbose,
        allow_delegation=False
    )
    
    # Agent 3: Editor
    editor = Agent(
        role="Editor",
        goal="Polish content for clarity, accuracy, and impact",
        backstory="""You are a meticulous editor with an eye for detail. You 
        check facts, improve clarity, fix any inconsistencies, and ensure the 
        final output is publication-ready.""",
        llm=llm,
        verbose=verbose,
        allow_delegation=False
    )
    
    return {
        "researcher": researcher,
        "writer": writer,
        "editor": editor
    }


def create_tasks(agents: Dict[str, Agent], topic: str) -> list:
    """
    Create the task pipeline for the research crew.
    
    Args:
        agents: Dictionary of agent instances
        topic: The research topic/question
        
    Returns:
        List of Task instances
    """
    
    # Task 1: Research
    research_task = Task(
        description=f"""Research the following topic thoroughly:

        TOPIC: {topic}

        Provide:
        1. Key facts and statistics
        2. Main trends or developments
        3. Notable examples or case studies
        4. Potential challenges or considerations
        
        Focus on accuracy and relevance. Cite sources where possible.""",
        expected_output="A comprehensive research brief with key findings, statistics, and insights.",
        agent=agents["researcher"]
    )
    
    # Task 2: Write
    writing_task = Task(
        description="""Using the research provided, write a clear and engaging brief.
        
        Requirements:
        - 300-500 words
        - Professional but accessible tone
        - Clear structure with introduction, body, and conclusion
        - Highlight the most important insights
        
        Do not add information beyond what was researched.""",
        expected_output="A well-written brief that clearly communicates the research findings.",
        agent=agents["writer"],
        context=[research_task]
    )
    
    # Task 3: Edit
    editing_task = Task(
        description="""Review and polish the written content.
        
        Check for:
        - Factual accuracy
        - Clarity and flow
        - Grammar and style
        - Appropriate tone
        
        Make improvements while preserving the writer's voice.
        Output the final, polished version.""",
        expected_output="A polished, publication-ready brief.",
        agent=agents["editor"],
        context=[writing_task]
    )
    
    return [research_task, writing_task, editing_task]


# =============================================================================
# CREW EXECUTION
# =============================================================================

@dataclass
class CrewResult:
    """Result from a crew execution"""
    success: bool
    output: str
    error: Optional[str]
    provider: str
    model: str
    task_outputs: Dict[str, str]


def run_research_crew(
    topic: str,
    provider: str = "ollama",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    verbose: bool = True,
    callback: Optional[callable] = None
) -> CrewResult:
    """
    Run the research crew on a given topic.
    
    Args:
        topic: The research topic or question
        provider: "ollama" or "openai"
        api_key: API key (required for OpenAI)
        model: Override default model
        verbose: Print agent activity
        callback: Optional callback for progress updates
        
    Returns:
        CrewResult with output and metadata
    """
    
    if not CREWAI_AVAILABLE:
        return CrewResult(
            success=False,
            output="",
            error="CrewAI not installed. Run: pip install crewai",
            provider=provider,
            model=model or PROVIDER_CONFIGS[provider].model,
            task_outputs={}
        )
    
    config = PROVIDER_CONFIGS.get(provider)
    model_name = model or config.model
    
    try:
        # Create LLM
        if callback:
            callback("status", f"Initializing {config.display_name}...")
        llm = get_llm(provider, api_key, model)
        
        # Create agents
        if callback:
            callback("status", "Creating agents...")
        agents = create_research_crew(llm, verbose=verbose)
        
        # Create tasks
        if callback:
            callback("status", "Setting up tasks...")
        tasks = create_tasks(agents, topic)
        
        # Create and run crew
        if callback:
            callback("status", "🔍 Researcher is gathering information...")
        
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=verbose
        )
        
        result = crew.kickoff()
        
        # Extract individual task outputs
        task_outputs = {}
        for i, task in enumerate(tasks):
            role = ["Researcher", "Writer", "Editor"][i]
            if hasattr(task, 'output') and task.output:
                task_outputs[role] = str(task.output)
        
        return CrewResult(
            success=True,
            output=str(result),
            error=None,
            provider=provider,
            model=model_name,
            task_outputs=task_outputs
        )
        
    except Exception as e:
        return CrewResult(
            success=False,
            output="",
            error=str(e),
            provider=provider,
            model=model_name,
            task_outputs={}
        )


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Command-line interface for running the research crew."""
    
    parser = argparse.ArgumentParser(
        description="Run a multi-agent research crew on a topic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with Ollama (free, local)
  python -m crews.research_crew --provider ollama --task "Research AI in healthcare"
  
  # Run with OpenAI (requires API key)
  export OPENAI_API_KEY=sk-...
  python -m crews.research_crew --provider openai --task "Research AI in healthcare"
  
  # Use a specific model
  python -m crews.research_crew --provider ollama --model mistral --task "Research quantum computing"
        """
    )
    
    parser.add_argument(
        "--task", "-t",
        required=True,
        help="The research topic or question"
    )
    
    parser.add_argument(
        "--provider", "-p",
        choices=["ollama", "openai"],
        default="ollama",
        help="LLM provider (default: ollama)"
    )
    
    parser.add_argument(
        "--model", "-m",
        help="Override default model (e.g., mistral, gpt-4o)"
    )
    
    parser.add_argument(
        "--api-key", "-k",
        help="API key (can also use OPENAI_API_KEY env var)"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress verbose agent output"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check provider availability and exit"
    )
    
    args = parser.parse_args()
    
    # Check mode
    if args.check:
        print("\n🔍 Checking provider availability...\n")
        
        available = get_available_providers()
        for name, config in PROVIDER_CONFIGS.items():
            status = "✅" if name in available else "❌"
            print(f"  {status} {config.display_name}")
            
            if name == "ollama" and name in available:
                if check_ollama_running():
                    print(f"      └─ Ollama is running")
                    if check_ollama_model("llama3.2"):
                        print(f"      └─ llama3.2 model available")
                    else:
                        print(f"      └─ ⚠️  llama3.2 not found. Run: ollama pull llama3.2")
                else:
                    print(f"      └─ ⚠️  Ollama not running. Start with: ollama serve")
            
            if name == "openai" and name in available:
                if os.getenv("OPENAI_API_KEY"):
                    print(f"      └─ API key found in environment")
                else:
                    print(f"      └─ ⚠️  No API key. Set OPENAI_API_KEY")
        
        print()
        return
    
    # Validate provider
    if args.provider == "ollama":
        if not OLLAMA_AVAILABLE:
            print("❌ Ollama support not installed. Run: pip install langchain-community")
            sys.exit(1)
        if not check_ollama_running():
            print("❌ Ollama is not running. Start with: ollama serve")
            sys.exit(1)
    
    if args.provider == "openai":
        if not OPENAI_AVAILABLE:
            print("❌ OpenAI support not installed. Run: pip install langchain-openai")
            sys.exit(1)
        if not args.api_key and not os.getenv("OPENAI_API_KEY"):
            print("❌ OpenAI API key required. Set OPENAI_API_KEY or use --api-key")
            sys.exit(1)
    
    # Run the crew
    config = PROVIDER_CONFIGS[args.provider]
    model = args.model or config.model
    
    print(f"\n{'='*60}")
    print(f"🤖 CrewAI Research Team")
    print(f"{'='*60}")
    print(f"Provider: {config.display_name}")
    print(f"Model:    {model}")
    print(f"Topic:    {args.task}")
    print(f"{'='*60}\n")
    
    def cli_callback(event_type, message):
        if event_type == "status":
            print(f"📌 {message}")
    
    result = run_research_crew(
        topic=args.task,
        provider=args.provider,
        api_key=args.api_key,
        model=args.model,
        verbose=not args.quiet,
        callback=cli_callback
    )
    
    print(f"\n{'='*60}")
    if result.success:
        print("✅ FINAL OUTPUT")
        print(f"{'='*60}\n")
        print(result.output)
    else:
        print("❌ ERROR")
        print(f"{'='*60}\n")
        print(result.error)
    
    print(f"\n{'='*60}")
    print(f"Provider: {result.provider} | Model: {result.model}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
