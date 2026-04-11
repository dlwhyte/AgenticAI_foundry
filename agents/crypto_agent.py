"""
LangChain Crypto Price Agent
============================

A simple LangChain agent that uses real-time data tools to get cryptocurrency prices.
Demonstrates tool-augmented reasoning with a single agent.

This contrasts with CrewAI's multi-agent approach:
- CrewAI: Multiple specialized agents collaborate (Researcher → Writer → Editor)
- LangChain: Single agent with tools (Agent + CoinGecko/Search Tool)

Tools used (in priority order):
1. CoinGecko API  — free, no API key, highly reliable live prices
2. DuckDuckGo     — fallback for general crypto questions
"""

import os
import time
import json
import urllib.request
from dataclasses import dataclass, field
from typing import Optional, Callable, List

from langchain_core.tools import Tool
from langchain.agents import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import PromptTemplate


# ---------------------------------------------------------------------------
# Telemetry & Result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AgentTelemetry:
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
    success: bool
    response: str
    telemetry: AgentTelemetry
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# CoinGecko tool
# ---------------------------------------------------------------------------

COIN_ID_MAP = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "solana": "solana", "sol": "solana",
    "cardano": "cardano", "ada": "cardano",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "xrp": "ripple", "ripple": "ripple",
    "polkadot": "polkadot", "dot": "polkadot",
    "avalanche": "avalanche-2", "avax": "avalanche-2",
    "chainlink": "chainlink", "link": "chainlink",
    "polygon": "matic-network", "matic": "matic-network",
    "litecoin": "litecoin", "ltc": "litecoin",
    "shiba inu": "shiba-inu", "shib": "shiba-inu",
    "uniswap": "uniswap", "uni": "uniswap",
    "stellar": "stellar", "xlm": "stellar",
}

DEFAULT_COINS = ["bitcoin", "ethereum", "solana"]


def _fetch_coingecko(coin_ids: List[str]) -> str:
    ids_param = ",".join(coin_ids)
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids_param}"
        "&vs_currencies=usd"
        "&include_24hr_change=true"
        "&include_market_cap=true"
    )
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    if not data:
        return "No price data returned from CoinGecko."

    lines = ["Live cryptocurrency prices (source: CoinGecko, updated every 60s):"]
    for coin_id, info in data.items():
        price = info.get("usd", "N/A")
        change = info.get("usd_24h_change", None)
        mcap = info.get("usd_market_cap", None)
        name = coin_id.replace("-", " ").title()
        price_str = f"${price:,.2f}" if isinstance(price, (int, float)) else str(price)
        change_str = f"  |  24h: {change:+.2f}%" if isinstance(change, (int, float)) else ""
        mcap_str = f"  |  Mkt cap: ${mcap/1e9:.1f}B" if isinstance(mcap, (int, float)) else ""
        lines.append(f"  {name}: {price_str}{change_str}{mcap_str}")
    return "\n".join(lines)


def coingecko_tool_func(query: str) -> str:
    query_lower = query.lower()
    coin_ids = []
    for name, cg_id in COIN_ID_MAP.items():
        if name in query_lower and cg_id not in coin_ids:
            coin_ids.append(cg_id)
    if not coin_ids:
        if any(w in query_lower for w in ["top", "all", "market", "list"]):
            coin_ids = ["bitcoin", "ethereum", "solana", "ripple", "cardano"]
        else:
            coin_ids = DEFAULT_COINS
    try:
        return _fetch_coingecko(coin_ids)
    except Exception as e:
        return f"CoinGecko API error: {e}"


def create_search_tool():
    coingecko = Tool(
        name="crypto_price_lookup",
        description=(
            "Fetch LIVE cryptocurrency prices, 24-hour change, and market cap from CoinGecko. "
            "Always use this tool first for any question about current crypto prices. "
            "Input: describe which coins you want, e.g. 'Bitcoin and Ethereum' or 'top 5 cryptos'."
        ),
        func=coingecko_tool_func,
    )
    tools = [coingecko]

    # Optional DuckDuckGo fallback for broader questions
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        ddg = DuckDuckGoSearchRun()
        _orig = ddg._run
        def safe_ddg(query):
            try:
                return _orig(query)
            except Exception as e:
                return f"Web search unavailable ({e}). crypto_price_lookup has the live data."
        tools.append(Tool(
            name="web_search",
            description="Search the web for crypto news or analysis. NOT for current prices — use crypto_price_lookup for that.",
            func=safe_ddg,
        ))
    except Exception:
        pass

    return tools


# ---------------------------------------------------------------------------
# LLM factory
# ---------------------------------------------------------------------------

def get_ollama_base_url() -> str:
    return os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def create_llm(provider: str = "openai", model_name: str = "gpt-4o-mini", api_key: Optional[str] = None):
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        env_key = os.environ.get("OPENAI_API_KEY", "")
        resolved_key = api_key or (env_key if not env_key.startswith("not-used-") else None)
        if not resolved_key:
            raise ValueError("OpenAI API key not found. Please enter your key in the sidebar.")
        return ChatOpenAI(model=model_name, temperature=0.3, api_key=resolved_key)
    else:
        from langchain_ollama import ChatOllama
        return ChatOllama(model=model_name, base_url=get_ollama_base_url(), temperature=0.3)


# ---------------------------------------------------------------------------
# Token counting & cost
# ---------------------------------------------------------------------------

def count_tokens(text: str, model_name: str = "gpt-4o-mini") -> int:
    try:
        import tiktoken
        try:
            enc = tiktoken.encoding_for_model(model_name)
        except KeyError:
            enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return len(text) // 4


def estimate_cost(input_tokens, output_tokens, provider, model_name):
    if provider != "openai":
        return 0.0
    pricing = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o":      {"input": 2.50, "output": 10.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    }
    r = pricing.get(model_name, {"input": 0.15, "output": 0.60})
    return (input_tokens / 1_000_000) * r["input"] + (output_tokens / 1_000_000) * r["output"]


# ---------------------------------------------------------------------------
# ReAct prompt — explicit instruction to always use the tool
# ---------------------------------------------------------------------------

REACT_PROMPT = """You are a helpful cryptocurrency assistant with access to real-time price data.

You have access to the following tools:

{tools}

IMPORTANT: Always use the crypto_price_lookup tool to get current prices. \
Never say you cannot provide current prices — the tool gives you live data directly from CoinGecko.

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


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_crypto_agent(
    query: str,
    provider: str = "openai",
    model_name: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    callback: Optional[Callable] = None,
    verbose: bool = True,
) -> AgentResult:
    telemetry = AgentTelemetry(query=query)
    telemetry.start_time = time.time()
    telemetry.status = "running"

    if callback:
        callback("status", "Initializing agent...")

    try:
        if callback:
            callback("status", f"Loading {provider} model: {model_name}...")
        llm = create_llm(provider, model_name, api_key=api_key)

        if callback:
            callback("status", "Setting up CoinGecko price tool...")
        tools = create_search_tool()

        prompt = PromptTemplate.from_template(REACT_PROMPT)

        if callback:
            callback("status", "Creating agent...")
        agent = create_react_agent(llm, tools, prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=verbose,
            handle_parsing_errors=True,
            max_iterations=5,
        )

        if callback:
            callback("status", "🔍 Agent is fetching live prices...")

        result = agent_executor.invoke({"input": query})
        response = result.get("output", "No response generated")

        telemetry.response = response
        telemetry.status = "complete"
        telemetry.input_tokens = count_tokens(query + REACT_PROMPT, model_name)
        telemetry.output_tokens = count_tokens(response, model_name)
        telemetry.total_tokens = telemetry.input_tokens + telemetry.output_tokens
        telemetry.tool_calls = 1
        telemetry.tools_used = [t.name for t in tools]
        telemetry.end_time = time.time()
        telemetry.duration_seconds = telemetry.end_time - telemetry.start_time
        telemetry.estimated_cost_usd = estimate_cost(
            telemetry.input_tokens, telemetry.output_tokens, provider, model_name
        )

        if callback:
            callback("status", "✅ Complete!")
            callback("telemetry", telemetry)

        return AgentResult(success=True, response=response, telemetry=telemetry)

    except Exception as e:
        telemetry.end_time = time.time()
        telemetry.duration_seconds = telemetry.end_time - telemetry.start_time
        telemetry.status = "error"
        if callback:
            callback("error", str(e))
        return AgentResult(success=False, response="", telemetry=telemetry, error=str(e))


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("LangChain Crypto Price Agent — Test Run")
    print("=" * 60)

    def status_callback(event_type, data):
        if event_type == "status":
            print(f"  → {data}")
        elif event_type == "telemetry":
            print(f"\n📊 Telemetry: {data.duration_seconds:.2f}s | {data.total_tokens} tokens | ${data.estimated_cost_usd:.6f}")

    result = run_crypto_agent(
        query="What is the current price of Bitcoin and Ethereum?",
        provider="openai",
        model_name="gpt-4o-mini",
        callback=status_callback,
        verbose=True,
    )

    print("\n" + "=" * 60)
    if result.success:
        print("✅ SUCCESS")
        print(f"\n{result.response}")
    else:
        print(f"❌ ERROR: {result.error}")
