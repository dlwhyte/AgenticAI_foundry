from __future__ import annotations
"""
CrewAI Research Team - Multi-Agent Demo with Telemetry
MIT Professional Education: Agentic AI

This module can be run standalone (CLI) or imported by Streamlit.
Enhanced with detailed telemetry: timing, token counts, API calls.

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
import time
from typing import Optional, Generator, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

# Ollama URL - auto-detect Docker vs local environment
def _get_ollama_host():
    """Determine the correct Ollama host URL."""
    # First check if explicitly set
    if os.environ.get("OLLAMA_HOST"):
        return os.environ.get("OLLAMA_HOST")
    
    # Try localhost first (works when running outside Docker)
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=1) as response:
            if response.status == 200:
                return "http://localhost:11434"
    except Exception:
        pass
    
    # Try host.docker.internal (works in Docker Desktop on Mac/Windows)
    try:
        import urllib.request
        req = urllib.request.Request("http://host.docker.internal:11434/api/tags")
        with urllib.request.urlopen(req, timeout=1) as response:
            if response.status == 200:
                return "http://host.docker.internal:11434"
    except Exception:
        pass
    
    # Default to localhost (will fail gracefully later with helpful message)
    return "http://localhost:11434"

OLLAMA_HOST = _get_ollama_host()

# CrewAI requires OPENAI_API_KEY to be set at import time, even if using Ollama.
# We set a dummy value here. The actual key is passed explicitly to ChatOpenAI.
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "not-used-we-pass-key-explicitly"

# CrewAI imports
try:
    from crewai import Agent, Task, Crew, Process, LLM
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

# LLM provider imports (for fallback/compatibility)
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Check if litellm is available (required for CrewAI's native LLM)
try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

OLLAMA_AVAILABLE = True  # Ollama support via CrewAI's native LLM class

# Token counting
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


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
    cost_per_1k_input_tokens: float
    cost_per_1k_output_tokens: float
    description: str


# Provider configurations with accurate pricing
PROVIDER_CONFIGS: Dict[str, ProviderConfig] = {
    "ollama": ProviderConfig(
        name="ollama",
        display_name="🏠 Ollama (Local)",
        model="llama3.2",
        requires_api_key=False,
        api_key_env=None,
        base_url=OLLAMA_HOST,
        cost_per_1k_input_tokens=0.0,
        cost_per_1k_output_tokens=0.0,
        description="Free, runs locally. Requires Ollama installed."
    ),
    "openai": ProviderConfig(
        name="openai",
        display_name="☁️ OpenAI",
        model="gpt-4o-mini",
        requires_api_key=True,
        api_key_env="OPENAI_API_KEY",
        base_url=None,
        cost_per_1k_input_tokens=0.00015,   # $0.15 per 1M input
        cost_per_1k_output_tokens=0.0006,   # $0.60 per 1M output
        description="Fast, high quality. Requires API key (~$0.01/run)."
    )
}


# =============================================================================
# TELEMETRY DATA STRUCTURES
# =============================================================================

@dataclass
class AgentTelemetry:
    """Telemetry data for a single agent's execution"""
    agent_name: str
    role: str
    start_time: float = 0.0
    end_time: float = 0.0
    duration_seconds: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    api_calls: int = 0
    task_description: str = ""
    output: str = ""
    reasoning_steps: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, running, complete, error
    error: Optional[str] = None


@dataclass
class CrewTelemetry:
    """Telemetry data for the entire crew execution"""
    start_time: float = 0.0
    end_time: float = 0.0
    total_duration_seconds: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    total_api_calls: int = 0
    estimated_cost_usd: float = 0.0
    agents: List[AgentTelemetry] = field(default_factory=list)
    provider: str = ""
    model: str = ""


@dataclass
class CrewResult:
    """Result from running a crew with telemetry"""
    success: bool
    output: str
    error: Optional[str]
    provider: str
    model: str
    task_outputs: Dict[str, str]
    telemetry: Optional[CrewTelemetry] = None


# =============================================================================
# TOKEN COUNTING
# =============================================================================

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Count tokens in text using tiktoken"""
    if not TIKTOKEN_AVAILABLE:
        # Rough estimate: ~4 chars per token
        return len(text) // 4
    
    try:
        # Map model names to tiktoken encodings
        if "gpt-4" in model or "gpt-3.5" in model:
            encoding = tiktoken.encoding_for_model(model)
        else:
            # Default to cl100k_base for other models (good approximation)
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        return len(text) // 4


def estimate_cost(input_tokens: int, output_tokens: int, provider: str) -> float:
    """Estimate cost based on token counts"""
    config = PROVIDER_CONFIGS.get(provider)
    if not config:
        return 0.0
    
    input_cost = (input_tokens / 1000) * config.cost_per_1k_input_tokens
    output_cost = (output_tokens / 1000) * config.cost_per_1k_output_tokens
    return input_cost + output_cost


# =============================================================================
# LLM FACTORY
# =============================================================================

def get_llm(provider: str, api_key: Optional[str] = None, model: Optional[str] = None):
    """
    Create an LLM instance based on provider.
    
    Args:
        provider: 'ollama' or 'openai'
        api_key: API key (required for OpenAI, ignored for Ollama)
        model: Model name (uses provider default if not specified)
    
    Returns:
        LLM instance ready for use with CrewAI
    """
    config = PROVIDER_CONFIGS.get(provider)
    if not config:
        raise ValueError(f"Unknown provider: {provider}")
    
    model_name = model or config.model
    
    if provider == "ollama":
        if not LITELLM_AVAILABLE:
            raise ImportError("litellm not installed. Run: pip install litellm")
        
        # Use CrewAI's native LLM class with ollama/ prefix
        return LLM(
            model=f"ollama/{model_name}",
            base_url=config.base_url
        )
    
    elif provider == "openai":
        if not LITELLM_AVAILABLE:
            raise ImportError("litellm not installed. Run: pip install litellm")
        
        # Get API key - prefer explicit parameter over env var
        # Ignore env var if it's our dummy placeholder
        env_key = os.getenv(config.api_key_env)
        if env_key and env_key.startswith("not-used-"):
            env_key = None
        key = api_key or env_key
        if not key:
            raise ValueError(f"OpenAI API key required. Enter it in the sidebar or set {config.api_key_env}.")
        
        # Use CrewAI's native LLM class
        return LLM(
            model=f"openai/{model_name}",
            api_key=key
        )
    
    else:
        raise ValueError(f"Provider {provider} not implemented")


def get_available_providers() -> Dict[str, ProviderConfig]:
    """Return configs for providers that are installed and available."""
    available = {}
    
    # Both providers require litellm for CrewAI's native LLM class
    if LITELLM_AVAILABLE:
        available["ollama"] = PROVIDER_CONFIGS["ollama"]
        available["openai"] = PROVIDER_CONFIGS["openai"]
    
    return available


def check_ollama_running() -> bool:
    """Check if Ollama server is running."""
    try:
        import urllib.request
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


def check_ollama_model(model: str = "llama3.2") -> bool:
    """Check if a specific model is available in Ollama."""
    try:
        import urllib.request
        import json
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            models = [m.get("name", "").split(":")[0] for m in data.get("models", [])]
            return model in models or f"{model}:latest" in [m.get("name", "") for m in data.get("models", [])]
    except Exception:
        return False
        
def get_ollama_models() -> list:
    """Get list of models available in the local Ollama installation."""
    try:
        import urllib.request
        import json
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            models = []
            for m in data.get("models", []):
                name = m.get("name", "")
                if name:
                    models.append(name)
                    short_name = name.split(":")[0]
                    if short_name != name and short_name not in models:
                        models.append(short_name)
            return sorted(set(models))
    except Exception:
        return ["llama3.2", "llama3.1", "mistral", "phi3", "gemma2"]

# =============================================================================
# AGENT DEFINITIONS
# =============================================================================

def create_research_crew(llm, verbose: bool = True) -> Dict[str, Agent]:
    """
    Create a research crew with three specialized agents.
    
    Returns dict of agents keyed by role name for easier telemetry tracking.
    """
    
    researcher = Agent(
        role="Research Analyst",
        goal="Gather comprehensive, accurate information on the given topic",
        backstory="""You are an experienced research analyst with a keen eye for detail.
        You excel at finding relevant information, identifying key trends, and 
        synthesizing complex data into clear insights. You always verify your sources
        and present balanced, factual information.""",
        verbose=verbose,
        allow_delegation=False,
        llm=llm
    )
    
    writer = Agent(
        role="Content Writer",
        goal="Transform research into clear, engaging content",
        backstory="""You are a skilled content writer who excels at making complex 
        topics accessible to general audiences. You write with clarity and precision,
        organizing information logically and maintaining reader engagement throughout.
        You adapt your tone to suit the subject matter while keeping content professional.""",
        verbose=verbose,
        allow_delegation=False,
        llm=llm
    )
    
    editor = Agent(
        role="Editor",
        goal="Polish content for clarity, accuracy, and professionalism",
        backstory="""You are a meticulous editor with years of experience refining 
        written content. You check for factual accuracy, improve clarity, fix any
        grammatical issues, and ensure the final output is polished and professional.
        You maintain the author's voice while elevating the quality of the writing.""",
        verbose=verbose,
        allow_delegation=False,
        llm=llm
    )
    
    return {
        "Researcher": researcher,
        "Writer": writer,
        "Editor": editor
    }


def create_tasks(agents: Dict[str, Agent], topic: str) -> List[Task]:
    """Create tasks for each agent with clear handoffs."""
    
    research_task = Task(
        description=f"""Research the following topic thoroughly: {topic}
        
        Your research should include:
        1. Key facts and statistics
        2. Current trends and developments
        3. Important considerations or challenges
        4. Notable examples or case studies (if relevant)
        
        Provide comprehensive but focused research that will serve as the 
        foundation for a well-written brief.""",
        expected_output="A detailed research brief with facts, statistics, and key insights",
        agent=agents["Researcher"]
    )
    
    writing_task = Task(
        description=f"""Using the research provided, write a clear and engaging brief about: {topic}
        
        Your brief should:
        1. Have a clear introduction that frames the topic
        2. Present key information in a logical flow
        3. Include relevant examples or data points
        4. Conclude with key takeaways
        
        Target length: 300-500 words. Make it accessible to a general business audience.""",
        expected_output="A well-structured, engaging brief of 300-500 words",
        agent=agents["Writer"],
        context=[research_task]
    )
    
    editing_task = Task(
        description="""Review and polish the written brief.
        
        Your editing should:
        1. Check for factual accuracy and consistency
        2. Improve clarity and readability
        3. Fix any grammatical or stylistic issues
        4. Ensure professional tone throughout
        5. Verify the brief is well-organized and flows logically
        
        Provide the final, polished version of the brief.""",
        expected_output="A polished, publication-ready brief",
        agent=agents["Editor"],
        context=[writing_task]
    )
    
    return [research_task, writing_task, editing_task]


# =============================================================================
# MAIN EXECUTION WITH TELEMETRY
# =============================================================================

def run_research_crew(
    topic: str,
    provider: str = "ollama",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    verbose: bool = True,
    callback: Optional[Callable] = None
) -> CrewResult:
    """
    Run the research crew on a topic with full telemetry.
    
    Args:
        topic: The topic to research
        provider: 'ollama' or 'openai'
        model: Model to use (defaults to provider's default)
        api_key: API key for OpenAI
        verbose: Whether to print verbose output
        callback: Optional callback for status updates
                  callback(event_type, data) where event_type is:
                  - "status": General status message
                  - "agent_start": Agent starting (data = AgentTelemetry)
                  - "agent_complete": Agent finished (data = AgentTelemetry)
                  - "telemetry": Full telemetry update (data = CrewTelemetry)
    
    Returns:
        CrewResult with output and telemetry
    """
    
    if not CREWAI_AVAILABLE:
        return CrewResult(
            success=False,
            output="",
            error="CrewAI not installed. Run: pip install crewai",
            provider=provider,
            model=model or PROVIDER_CONFIGS[provider].model,
            task_outputs={},
            telemetry=None
        )
    
    config = PROVIDER_CONFIGS.get(provider)
    model_name = model or config.model
    
    # Initialize telemetry
    crew_telemetry = CrewTelemetry(
        provider=provider,
        model=model_name,
        start_time=time.time()
    )
    
    # Initialize agent telemetry
    agent_names = ["Researcher", "Writer", "Editor"]
    agent_roles = ["Research Analyst", "Content Writer", "Editor"]
    task_descriptions = [
        f"Research the topic: {topic}",
        "Write a clear brief from the research",
        "Polish and edit the final brief"
    ]
    
    for i, name in enumerate(agent_names):
        crew_telemetry.agents.append(AgentTelemetry(
            agent_name=name,
            role=agent_roles[i],
            task_description=task_descriptions[i],
            status="pending"
        ))
    
    # For OpenAI: set the real API key in environment so CrewAI can use it
    _original_key = None
    if provider == "openai" and api_key:
        _original_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = api_key
    
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
        
        # Create crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=verbose
        )
        
        # Run each agent and capture telemetry
        # Note: CrewAI runs sequentially, so we track timing around kickoff
        # For more granular tracking, we'd need to hook into CrewAI callbacks
        
        if callback:
            callback("status", "🔍 Researcher is gathering information...")
            crew_telemetry.agents[0].status = "running"
            crew_telemetry.agents[0].start_time = time.time()
            callback("agent_start", crew_telemetry.agents[0])
        
        # Run the crew
        result = crew.kickoff()
        
        crew_telemetry.end_time = time.time()
        crew_telemetry.total_duration_seconds = crew_telemetry.end_time - crew_telemetry.start_time
        
        # Extract individual task outputs and estimate tokens
        task_outputs = {}
        total_input_tokens = 0
        total_output_tokens = 0
        
        # Estimate tokens for the input (topic + agent prompts)
        base_input = topic + " ".join([a.backstory for a in agents.values()])
        base_input_tokens = count_tokens(base_input, model_name)
        
        for i, task in enumerate(tasks):
            name = agent_names[i]
            agent_telemetry = crew_telemetry.agents[i]
            
            if hasattr(task, 'output') and task.output:
                output_text = str(task.output)
                task_outputs[name] = output_text
                
                # Estimate tokens
                output_tokens = count_tokens(output_text, model_name)
                # Input includes previous outputs as context
                context_tokens = sum(count_tokens(task_outputs.get(agent_names[j], ""), model_name) 
                                    for j in range(i))
                input_tokens = base_input_tokens + context_tokens
                
                agent_telemetry.output = output_text
                agent_telemetry.input_tokens = input_tokens
                agent_telemetry.output_tokens = output_tokens
                agent_telemetry.total_tokens = input_tokens + output_tokens
                agent_telemetry.api_calls = 1  # Minimum 1 call per agent
                agent_telemetry.status = "complete"
                
                total_input_tokens += input_tokens
                total_output_tokens += output_tokens
            else:
                agent_telemetry.status = "complete"
                agent_telemetry.output = "(No output captured)"
        
        # Estimate timing per agent based on output tokens (proxy for work done)
        # More tokens = more generation time (roughly proportional)
        total_time = crew_telemetry.total_duration_seconds
        total_output = sum(a.output_tokens for a in crew_telemetry.agents) or 1  # avoid div by zero
        
        cumulative_time = 0
        for i, agent_telemetry in enumerate(crew_telemetry.agents):
            # Weight time by proportion of output tokens
            token_ratio = agent_telemetry.output_tokens / total_output if total_output > 0 else 0.33
            agent_time = total_time * token_ratio
            
            agent_telemetry.start_time = crew_telemetry.start_time + cumulative_time
            agent_telemetry.duration_seconds = agent_time
            agent_telemetry.end_time = agent_telemetry.start_time + agent_time
            cumulative_time += agent_time
        
        # Update crew telemetry totals
        crew_telemetry.total_input_tokens = total_input_tokens
        crew_telemetry.total_output_tokens = total_output_tokens
        crew_telemetry.total_tokens = total_input_tokens + total_output_tokens
        crew_telemetry.total_api_calls = sum(a.api_calls for a in crew_telemetry.agents)
        crew_telemetry.estimated_cost_usd = estimate_cost(total_input_tokens, total_output_tokens, provider)
        
        if callback:
            callback("telemetry", crew_telemetry)
        
        return CrewResult(
            success=True,
            output=str(result),
            error=None,
            provider=provider,
            model=model_name,
            task_outputs=task_outputs,
            telemetry=crew_telemetry
        )
        
    except Exception as e:
        crew_telemetry.end_time = time.time()
        crew_telemetry.total_duration_seconds = crew_telemetry.end_time - crew_telemetry.start_time
        
        return CrewResult(
            success=False,
            output="",
            error=str(e),
            provider=provider,
            model=model_name,
            task_outputs={},
            telemetry=crew_telemetry
        )
    
    finally:
        # Restore original API key
        if provider == "openai" and _original_key is not None:
            os.environ["OPENAI_API_KEY"] = _original_key


# =============================================================================
# CLI INTERFACE
# =============================================================================

def print_telemetry(telemetry: CrewTelemetry):
    """Print formatted telemetry report."""
    print("\n" + "=" * 70)
    print("📊 TELEMETRY REPORT")
    print("=" * 70)
    
    print(f"\n⏱️  Total Duration: {telemetry.total_duration_seconds:.1f} seconds")
    print(f"🔢 Total Tokens: {telemetry.total_tokens:,}")
    print(f"   ├─ Input:  {telemetry.total_input_tokens:,}")
    print(f"   └─ Output: {telemetry.total_output_tokens:,}")
    print(f"📞 Total API Calls: {telemetry.total_api_calls}")
    if telemetry.provider == "openai":
        print(f"💰 Estimated Cost: ${telemetry.estimated_cost_usd:.4f}")
    else:
        print(f"💰 Cost: Free (local)")
    
    print("\n" + "-" * 70)
    print("AGENT BREAKDOWN")
    print("-" * 70)
    
    for agent in telemetry.agents:
        print(f"\n{'🔍' if agent.agent_name == 'Researcher' else '✍️' if agent.agent_name == 'Writer' else '📝'} {agent.agent_name} ({agent.role})")
        print(f"   ├─ Duration: {agent.duration_seconds:.1f}s")
        print(f"   ├─ Tokens: {agent.total_tokens:,} (in: {agent.input_tokens:,}, out: {agent.output_tokens:,})")
        print(f"   ├─ API Calls: {agent.api_calls}")
        print(f"   └─ Status: {agent.status}")
    
    print("\n" + "=" * 70)


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
        type=str,
        help="The topic/task for the research crew"
    )
    
    parser.add_argument(
        "--provider", "-p",
        type=str,
        choices=["ollama", "openai"],
        default="ollama",
        help="LLM provider to use (default: ollama)"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        help="Model to use (default: provider's default model)"
    )
    
    parser.add_argument(
        "--api-key", "-k",
        type=str,
        help="API key (can also use OPENAI_API_KEY env var)"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress verbose output"
    )
    
    parser.add_argument(
        "--no-telemetry",
        action="store_true",
        help="Don't print telemetry report"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check provider availability and exit"
    )
    
    args = parser.parse_args()
    
    # Check mode
    if args.check:
        print("🔍 Checking provider availability...\n")
        available = get_available_providers()
        
        for name, config in PROVIDER_CONFIGS.items():
            if name in available:
                print(f"  ✅ {config.display_name}")
            else:
                print(f"  ❌ {config.display_name} (not installed)")
            
            if name == "ollama" and name in available:
                if check_ollama_running():
                    print(f"      └─ Ollama is running")
                    if check_ollama_model():
                        print(f"      └─ llama3.2 model available")
                    else:
                        print(f"      └─ ⚠️  llama3.2 not found. Run: ollama pull llama3.2")
                else:
                    print(f"      └─ ⚠️  Ollama not running. Start with: ollama serve")
            
            if name == "openai" and name in available:
                env_key = os.getenv("OPENAI_API_KEY")
                if env_key and not env_key.startswith("not-used-"):
                    print(f"      └─ API key found in environment")
                else:
                    print(f"      └─ ⚠️  No API key. Set OPENAI_API_KEY or enter in sidebar")
        
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
        env_key = os.getenv("OPENAI_API_KEY")
        has_real_env_key = env_key and not env_key.startswith("not-used-")
        if not args.api_key and not has_real_env_key:
            print("❌ OpenAI API key required. Set OPENAI_API_KEY or use --api-key")
            sys.exit(1)
    
    # Require task
    if not args.task:
        print("❌ Please provide a task with --task or -t")
        sys.exit(1)
    
    # Run the crew
    config = PROVIDER_CONFIGS[args.provider]
    print(f"\n{'=' * 70}")
    print(f"🤖 CrewAI Research Team")
    print(f"{'=' * 70}")
    print(f"Provider: {config.display_name}")
    print(f"Model:    {args.model or config.model}")
    print(f"Topic:    {args.task}")
    print(f"{'=' * 70}\n")
    
    result = run_research_crew(
        topic=args.task,
        provider=args.provider,
        model=args.model,
        api_key=args.api_key,
        verbose=not args.quiet
    )
    
    if result.success:
        print(f"\n{'=' * 70}")
        print("✅ FINAL OUTPUT")
        print(f"{'=' * 70}\n")
        print(result.output)
        
        if not args.no_telemetry and result.telemetry:
            print_telemetry(result.telemetry)
    else:
        print(f"\n❌ Error: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
