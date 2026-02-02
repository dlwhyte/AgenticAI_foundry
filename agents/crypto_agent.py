"""
LangChain Crypto Price Agent
============================

A simple LangChain agent that uses web search to get current cryptocurrency prices.
Demonstrates tool-augmented reasoning with a single agent.

This contrasts with CrewAI's multi-agent approach:
- CrewAI: Multiple specialized agents collaborate (Researcher → Writer → Editor)
- LangChain: Single agent with tools (Agent + Web Search Tool)
"""

import os
import time
from dataclasses import dataclass, field
from typing import Optional, Callable, List

# LangChain imports
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate


@dataclass
class AgentTelemetry:
    """Telemetry data for the agent execution."""
    start_time: float = 0
    end_time: float = 0
    duration_seconds: float = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    tool_calls: int = 0
    tools_used: List[str] = field(default_factory=list)
    status: str = "pending"
    query: str = ""
    response: str = ""
    thought_process: str = ""
    estimated_cost_usd: float = 0.0


@dataclass
class AgentResult:
    """Result from running the crypto agent."""
    success: bool
    response: str
    telemetry: AgentTelemetry
    error: Optional[str] = None


def get_ollama_base_url() -> str:
    """Get the Ollama base URL, handling Docker networking."""
    return os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def create_search_tool():
    """Create a DuckDuckGo search tool."""
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search = DuckDuckGoSearchRun()
        return search
    except ImportError:
        # Fallback: create a mock tool for demo purposes
        def mock_search(query: str) -> str:
            return f"[Mock search result for: {query}] - Search tool not available. Install duckduckgo-search package."
        
        return Tool(
            name="web_search",
            description="Search the web for current information",
            func=mock_search
        )


def create_llm(provider: str = "openai", model_name: str = "gpt-4o-mini"):
    """
    Create an LLM instance based on provider.
    
    Args:
        provider: "openai" or "ollama"
        model_name: Model name (e.g., "gpt-4o-mini", "llama3.2")
    
    Returns:
        LLM instance
    """
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model_name,
            temperature=0.3
        )
    else:  # ollama
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=model_name,
            base_url=get_ollama_base_url(),
            temperature=0.3
        )


def count_tokens(text: str, model_name: str = "gpt-4o-mini") -> int:
    """Estimate token count for a string."""
    try:
        import tiktoken
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except ImportError:
        # Rough estimate: ~4 characters per token
        return len(text) // 4


def estimate_cost(input_tokens: int, output_tokens: int, provider: str, model_name: str) -> float:
    """Estimate cost based on token usage."""
    if provider != "openai":
        return 0.0  # Ollama is free
    
    # Pricing per 1M tokens (approximate)
    pricing = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    }
    
    rates = pricing.get(model_name, {"input": 0.15, "output": 0.60})
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    
    return input_cost + output_cost


# ReAct prompt template for the agent
REACT_PROMPT = """You are a helpful assistant that can search the web for current cryptocurrency prices.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


def run_crypto_agent(
    query: str,
    provider: str = "openai",
    model_name: str = "gpt-4o-mini",
    callback: Optional[Callable] = None,
    verbose: bool = True
) -> AgentResult:
    """
    Run the crypto price agent.
    
    Args:
        query: User's question (e.g., "What's the current price of Bitcoin?")
        provider: "openai" or "ollama"
        model_name: Model to use
        callback: Optional callback for status updates
        verbose: Whether to print verbose output
    
    Returns:
        AgentResult with response and telemetry
    """
    telemetry = AgentTelemetry(query=query)
    telemetry.start_time = time.time()
    telemetry.status = "running"
    
    if callback:
        callback("status", "Initializing agent...")
    
    try:
        # Create LLM
        if callback:
            callback("status", f"Loading {provider} model: {model_name}...")
        llm = create_llm(provider, model_name)
        
        # Create search tool
        if callback:
            callback("status", "Setting up web search tool...")
        search_tool = create_search_tool()
        tools = [search_tool]
        
        # Create the prompt
        prompt = PromptTemplate.from_template(REACT_PROMPT)
        
        # Create the agent
        if callback:
            callback("status", "Creating agent...")
        agent = create_react_agent(llm, tools, prompt)
        
        # Create executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=verbose,
            handle_parsing_errors=True,
            max_iterations=5
        )
        
        # Run the agent
        if callback:
            callback("status", "🔍 Agent is thinking and searching...")
        
        result = agent_executor.invoke({"input": query})
        
        # Extract response
        response = result.get("output", "No response generated")
        telemetry.response = response
        telemetry.status = "complete"
        
        # Estimate tokens (rough)
        telemetry.input_tokens = count_tokens(query + REACT_PROMPT, model_name)
        telemetry.output_tokens = count_tokens(response, model_name)
        telemetry.total_tokens = telemetry.input_tokens + telemetry.output_tokens
        
        # Count tool usage
        telemetry.tool_calls = 1  # At minimum, we called the search
        telemetry.tools_used = ["web_search"]
        
        # Calculate timing and cost
        telemetry.end_time = time.time()
        telemetry.duration_seconds = telemetry.end_time - telemetry.start_time
        telemetry.estimated_cost_usd = estimate_cost(
            telemetry.input_tokens, 
            telemetry.output_tokens, 
            provider, 
            model_name
        )
        
        if callback:
            callback("status", "✅ Complete!")
            callback("telemetry", telemetry)
        
        return AgentResult(
            success=True,
            response=response,
            telemetry=telemetry
        )
        
    except Exception as e:
        telemetry.end_time = time.time()
        telemetry.duration_seconds = telemetry.end_time - telemetry.start_time
        telemetry.status = "error"
        
        error_msg = str(e)
        
        if callback:
            callback("error", error_msg)
        
        return AgentResult(
            success=False,
            response="",
            telemetry=telemetry,
            error=error_msg
        )


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("LangChain Crypto Price Agent - Test Run")
    print("=" * 60)
    
    def status_callback(event_type, data):
        if event_type == "status":
            print(f"  → {data}")
        elif event_type == "telemetry":
            print(f"\n📊 Telemetry:")
            print(f"   Duration: {data.duration_seconds:.2f}s")
            print(f"   Tokens: {data.total_tokens}")
            print(f"   Cost: ${data.estimated_cost_usd:.6f}")
    
    result = run_crypto_agent(
        query="What is the current price of Bitcoin and Ethereum?",
        provider="openai",  # Change to "ollama" if needed
        model_name="gpt-4o-mini",
        callback=status_callback,
        verbose=True
    )
    
    print("\n" + "=" * 60)
    if result.success:
        print("✅ SUCCESS")
        print(f"\n{result.response}")
    else:
        print(f"❌ ERROR: {result.error}")
