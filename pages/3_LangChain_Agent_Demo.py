"""
LangChain Agent Demo - Crypto Price Lookup
==========================================

This page demonstrates a LangChain agent that uses web search
to get current cryptocurrency prices.

Key Concepts:
- Single agent with tool access (vs CrewAI's multi-agent collaboration)
- ReAct pattern: Reasoning + Acting
- Real-time data via DuckDuckGo search
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.crypto_agent import run_crypto_agent, AgentTelemetry


def check_openai_key() -> bool:
    """Check if OpenAI API key is configured."""
    return bool(os.environ.get("OPENAI_API_KEY"))


def check_ollama_running() -> bool:
    """Check if Ollama is running and accessible."""
    import urllib.request
    import urllib.error
    
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    
    try:
        # Try host.docker.internal first (for Docker)
        for host in [ollama_host, "http://host.docker.internal:11434"]:
            try:
                req = urllib.request.Request(f"{host}/api/tags", method="GET")
                with urllib.request.urlopen(req, timeout=3) as response:
                    if response.status == 200:
                        return True
            except:
                continue
        return False
    except:
        return False


def render_telemetry(telemetry: AgentTelemetry):
    """Render telemetry data."""
    st.subheader("📊 Telemetry")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Duration", f"{telemetry.duration_seconds:.2f}s")
    with col2:
        st.metric("Total Tokens", f"{telemetry.total_tokens:,}")
    with col3:
        st.metric("Tool Calls", telemetry.tool_calls)
    with col4:
        if telemetry.estimated_cost_usd > 0:
            st.metric("Est. Cost", f"${telemetry.estimated_cost_usd:.6f}")
        else:
            st.metric("Est. Cost", "Free (local)")
    
    # Token breakdown
    with st.expander("Token Breakdown"):
        st.write(f"**Input Tokens:** {telemetry.input_tokens:,}")
        st.write(f"**Output Tokens:** {telemetry.output_tokens:,}")
        st.write(f"**Tools Used:** {', '.join(telemetry.tools_used) if telemetry.tools_used else 'None'}")


def main():
    st.set_page_config(
        page_title="LangChain Agent Demo",
        page_icon="🔗",
        layout="wide"
    )
    
    st.title("🔗 LangChain Agent Demo")
    st.markdown("**Single agent with web search tool** - Get real-time crypto prices")
    
    # Explanation
    with st.expander("ℹ️ How This Works", expanded=False):
        st.markdown("""
        ### LangChain vs CrewAI
        
        | Aspect | This Demo (LangChain) | Multi-Agent Demo (CrewAI) |
        |--------|----------------------|---------------------------|
        | **Agents** | Single agent | Multiple agents (Researcher → Writer → Editor) |
        | **Approach** | Agent + Tools | Agent collaboration |
        | **Pattern** | ReAct (Reason + Act) | Sequential task handoff |
        
        ### The ReAct Pattern
        
        ```
        Question → Thought → Action → Observation → ... → Final Answer
        ```
        
        The agent:
        1. **Thinks** about what it needs to do
        2. **Acts** by calling a tool (web search)
        3. **Observes** the result
        4. **Repeats** if needed
        5. **Answers** when it has enough information
        """)
    
    st.divider()
    
    # Configuration
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Configuration")
        
        # Provider selection
        provider = st.radio(
            "LLM Provider",
            ["OpenAI", "Ollama (Local)"],
            help="OpenAI requires API key. Ollama runs locally for free."
        )
        
        provider_key = "openai" if provider == "OpenAI" else "ollama"
        
        # Model selection based on provider
        if provider_key == "openai":
            model = st.selectbox(
                "Model",
                ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
                index=0
            )
            
            # Check API key
            if not check_openai_key():
                st.warning("⚠️ OPENAI_API_KEY not set")
                api_key = st.text_input("Enter API Key:", type="password")
                if api_key:
                    os.environ["OPENAI_API_KEY"] = api_key
                    st.success("✅ API key set for this session")
        else:
            model = st.selectbox(
                "Model",
                ["llama3.2", "llama3.1", "mistral", "phi3"],
                index=0
            )
            
            # Check Ollama
            if not check_ollama_running():
                st.warning("⚠️ Ollama not detected. Make sure it's running.")
    
    with col2:
        st.subheader("💬 Query")
        
        # Example queries
        st.markdown("**Try these examples:**")
        example_col1, example_col2 = st.columns(2)
        
        with example_col1:
            if st.button("📈 Bitcoin & Ethereum prices", use_container_width=True):
                st.session_state.query = "What is the current price of Bitcoin and Ethereum?"
            if st.button("🪙 Top 5 cryptos by market cap", use_container_width=True):
                st.session_state.query = "What are the top 5 cryptocurrencies by market cap and their current prices?"
        
        with example_col2:
            if st.button("📊 Bitcoin vs last week", use_container_width=True):
                st.session_state.query = "What is Bitcoin's current price and how has it changed in the last week?"
            if st.button("💡 Solana price today", use_container_width=True):
                st.session_state.query = "What is the current price of Solana?"
        
        # Query input
        query = st.text_area(
            "Your question:",
            value=st.session_state.get("query", "What is the current price of Bitcoin and Ethereum?"),
            height=80
        )
        
        run_button = st.button("🚀 Run Agent", type="primary", use_container_width=True)
    
    st.divider()
    
    # Run the agent
    if run_button and query:
        status_container = st.empty()
        progress_bar = st.progress(0)
        
        # Status callback
        def status_callback(event_type, data):
            if event_type == "status":
                status_container.info(f"🔄 {data}")
                # Update progress roughly
                if "Initializing" in data:
                    progress_bar.progress(10)
                elif "Loading" in data:
                    progress_bar.progress(25)
                elif "Setting up" in data:
                    progress_bar.progress(40)
                elif "Creating" in data:
                    progress_bar.progress(55)
                elif "thinking" in data:
                    progress_bar.progress(70)
                elif "Complete" in data:
                    progress_bar.progress(100)
        
        # Run agent
        result = run_crypto_agent(
            query=query,
            provider=provider_key,
            model_name=model,
            callback=status_callback,
            verbose=False
        )
        
        # Clear status
        status_container.empty()
        progress_bar.empty()
        
        if result.success:
            st.success("✅ Agent completed successfully!")
            
            # Response
            st.subheader("💬 Response")
            st.markdown(result.response)
            
            # Telemetry
            st.divider()
            render_telemetry(result.telemetry)
            
        else:
            st.error(f"❌ Error: {result.error}")
            
            # Troubleshooting
            with st.expander("🔧 Troubleshooting"):
                if "OPENAI_API_KEY" in str(result.error):
                    st.markdown("**Solution:** Set your OpenAI API key above or switch to Ollama.")
                elif "Connection" in str(result.error) or "refused" in str(result.error):
                    st.markdown("""
                    **Possible issues:**
                    - Ollama not running: Start it with `ollama serve`
                    - Docker networking: Try setting `OLLAMA_HOST=http://host.docker.internal:11434`
                    """)
                else:
                    st.markdown(f"**Error details:** `{result.error}`")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <strong>LangChain Agent Demo</strong> | Part of AgenticAI Foundry<br>
        Demonstrates tool-augmented single-agent reasoning
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
