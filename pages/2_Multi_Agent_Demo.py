"""
CrewAI Multi-Agent Demo - Streamlit Page with Telemetry
MIT Professional Education: Agentic AI

Watch three AI agents collaborate in real-time with full telemetry:
- Timing per phase
- Token counts
- API calls
- Cost estimates
- Agent outputs
"""

import streamlit as st
import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import crew logic
try:
    from crews.research_crew import (
        run_research_crew,
        get_available_providers,
        check_ollama_running,
        check_ollama_model,
        PROVIDER_CONFIGS
    )
    CREW_AVAILABLE = True
except ImportError as e:
    CREW_AVAILABLE = False
    IMPORT_ERROR = str(e)


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Multi-Agent Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #6c757d;
    }
    .agent-researcher { border-left-color: #0066cc; }
    .agent-writer { border-left-color: #28a745; }
    .agent-editor { border-left-color: #9933cc; }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .status-pending { background: #e9ecef; color: #6c757d; }
    .status-running { background: #cce5ff; color: #004085; }
    .status-done { background: #d4edda; color: #155724; }
    
    .telemetry-box {
        background: #1a1a2e;
        color: #00ff88;
        font-family: 'Monaco', 'Consolas', monospace;
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A5F;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.25rem;
    }
    
    .output-box {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        line-height: 1.6;
    }
    
    .agent-output-box {
        background: #fafafa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .phase-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 0.5rem;
    }
    
    .token-badge {
        background: #e3f2fd;
        color: #1565c0;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .time-badge {
        background: #fff3e0;
        color: #e65100;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .cost-badge {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_duration(seconds: float) -> str:
    """Format seconds into readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}m {secs:.0f}s"


def format_tokens(count: int) -> str:
    """Format token count."""
    if count >= 1000:
        return f"{count/1000:.1f}k"
    return str(count)


def format_cost(cost: float) -> str:
    """Format cost in USD."""
    if cost == 0:
        return "Free"
    elif cost < 0.01:
        return f"${cost:.4f}"
    else:
        return f"${cost:.2f}"


# =============================================================================
# MAIN PAGE
# =============================================================================

# Header
st.markdown('<p class="main-header">🤖 Multi-Agent Research Demo</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Watch three AI agents collaborate with full telemetry</p>', unsafe_allow_html=True)

# Check if crew is available
if not CREW_AVAILABLE:
    st.error(f"""
    **CrewAI dependencies not installed.**
    
    Run: `pip install crewai langchain-community langchain-openai`
    
    Error: {IMPORT_ERROR}
    """)
    st.stop()

# Get available providers
available_providers = get_available_providers()

if not available_providers:
    st.error("""
    **No LLM providers available.**
    
    Install at least one:
    - For Ollama (free, local): `pip install langchain-community`
    - For OpenAI (paid, cloud): `pip install langchain-openai`
    """)
    st.stop()


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Provider selection
    provider_options = list(available_providers.keys())
    provider_names = [PROVIDER_CONFIGS[p].display_name for p in provider_options]
    
    provider_choice = st.selectbox(
        "Select Provider",
        options=provider_options,
        format_func=lambda x: PROVIDER_CONFIGS[x].display_name,
        help="Choose between local (Ollama) or cloud (OpenAI) AI"
    )
    
    config = PROVIDER_CONFIGS[provider_choice]
    st.caption(config.description)
    
    # Provider-specific settings
    if provider_choice == "ollama":
        # Check Ollama status
        ollama_running = check_ollama_running()
        if ollama_running:
            st.success("✅ Ollama is running")
            if check_ollama_model():
                st.caption("llama3.2 model ready")
            else:
                st.warning("⚠️ llama3.2 not found. Run: `ollama pull llama3.2`")
        else:
            st.error("❌ Ollama not running. Start with: `ollama serve`")
        
        ollama_model = st.selectbox(
            "Model",
            options=["llama3.2", "llama3.1", "mistral", "phi3", "gemma2"],
            help="Select Ollama model"
        )
        api_key = None
        
    elif provider_choice == "openai":
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key or set OPENAI_API_KEY environment variable"
        )
        # Filter out placeholder
        if api_key and api_key.startswith("not-used-"):
            api_key = ""
            
        if not api_key:
            st.warning("⚠️ API key required")
        
        openai_model = st.selectbox(
            "Model",
            options=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            help="Select OpenAI model"
        )
    
    st.divider()
    
    # Telemetry options
    st.subheader("📊 Display Options")
    show_agent_outputs = st.checkbox("Show individual agent outputs", value=True)
    show_telemetry_details = st.checkbox("Show detailed telemetry", value=True)


# =============================================================================
# MAIN CONTENT
# =============================================================================

# How it works
with st.expander("ℹ️ How it works", expanded=False):
    st.markdown("""
    This demo runs **three AI agents** that collaborate sequentially:
    
    1. **🔍 Researcher** - Gathers facts, statistics, and key insights
    2. **✍️ Writer** - Transforms research into clear, engaging prose  
    3. **📝 Editor** - Polishes for clarity, accuracy, and professionalism
    
    Each agent passes their work to the next, similar to a real content team.
    
    **Telemetry tracked:**
    - ⏱️ Duration per agent
    - 🔢 Token counts (input/output)
    - 📞 API calls
    - 💰 Cost estimates
    """)

# Topic input
st.subheader("📝 Research Topic")

col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_area(
        "What would you like the team to research?",
        value=st.session_state.get("topic", ""),
        placeholder="Example: The impact of artificial intelligence on healthcare diagnostics",
        height=100,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**Example Topics:**")
    examples = [
        "AI in healthcare",
        "Remote work trends", 
        "Sustainable energy",
        "Quantum computing",
        "AI agents in customer service"
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.topic = f"Research the current state of {ex.lower()}, including key developments, challenges, and future outlook."
            st.rerun()

# Use session state topic if set
if "topic" in st.session_state and not topic:
    topic = st.session_state.topic

# Validation
can_run = bool(topic)
if provider_choice == "openai" and not api_key:
    can_run = False
if provider_choice == "ollama" and not check_ollama_running():
    can_run = False

# Run button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_button = st.button(
        "🚀 Run Research Crew",
        type="primary",
        disabled=not can_run,
        use_container_width=True
    )


# =============================================================================
# EXECUTION & RESULTS
# =============================================================================

if run_button and can_run:
    
    # Create containers for live updates
    st.divider()
    
    # Summary metrics row
    metrics_container = st.container()
    
    # Agent status cards
    st.subheader("👥 Agent Activity")
    agent_cols = st.columns(3)
    
    with agent_cols[0]:
        researcher_card = st.empty()
        researcher_card.markdown("""
        <div class="agent-card agent-researcher">
            <strong>🔍 Researcher</strong><br/>
            <span class="status-badge status-pending">Waiting...</span>
        </div>
        """, unsafe_allow_html=True)
    
    with agent_cols[1]:
        writer_card = st.empty()
        writer_card.markdown("""
        <div class="agent-card agent-writer">
            <strong>✍️ Writer</strong><br/>
            <span class="status-badge status-pending">Waiting...</span>
        </div>
        """, unsafe_allow_html=True)
    
    with agent_cols[2]:
        editor_card = st.empty()
        editor_card.markdown("""
        <div class="agent-card agent-editor">
            <strong>📝 Editor</strong><br/>
            <span class="status-badge status-pending">Waiting...</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Output containers
    output_container = st.container()
    telemetry_container = st.container()
    
    # Prepare parameters
    run_params = {
        "topic": topic,
        "provider": provider_choice,
        "verbose": False
    }
    
    if provider_choice == "ollama":
        run_params["model"] = ollama_model
    elif provider_choice == "openai":
        run_params["api_key"] = api_key
        run_params["model"] = openai_model
    
    # Update UI to show running
    status_text.text("🔍 Researcher is gathering information...")
    researcher_card.markdown("""
    <div class="agent-card agent-researcher">
        <strong>🔍 Researcher</strong><br/>
        <span class="status-badge status-running">Working... ⏳</span>
    </div>
    """, unsafe_allow_html=True)
    progress_bar.progress(10)
    
    # Run the crew
    start_time = time.time()
    with st.spinner("Agents are working..."):
        result = run_research_crew(**run_params)
    elapsed = time.time() - start_time
    
    # Update UI based on result
    if result.success and result.telemetry:
        telemetry = result.telemetry
        
        # Update agent cards with telemetry
        researcher_data = telemetry.agents[0] if len(telemetry.agents) > 0 else None
        writer_data = telemetry.agents[1] if len(telemetry.agents) > 1 else None
        editor_data = telemetry.agents[2] if len(telemetry.agents) > 2 else None
        
        # Researcher complete
        researcher_card.markdown(f"""
        <div class="agent-card agent-researcher">
            <strong>🔍 Researcher</strong>
            <span class="status-badge status-done">Complete ✓</span><br/>
            <span class="time-badge">⏱️ {format_duration(researcher_data.duration_seconds if researcher_data else 0)}</span>
            <span class="token-badge">🔢 {format_tokens(researcher_data.total_tokens if researcher_data else 0)} tokens</span>
        </div>
        """, unsafe_allow_html=True)
        progress_bar.progress(40)
        
        # Writer complete
        writer_card.markdown(f"""
        <div class="agent-card agent-writer">
            <strong>✍️ Writer</strong>
            <span class="status-badge status-done">Complete ✓</span><br/>
            <span class="time-badge">⏱️ {format_duration(writer_data.duration_seconds if writer_data else 0)}</span>
            <span class="token-badge">🔢 {format_tokens(writer_data.total_tokens if writer_data else 0)} tokens</span>
        </div>
        """, unsafe_allow_html=True)
        progress_bar.progress(70)
        
        # Editor complete
        editor_card.markdown(f"""
        <div class="agent-card agent-editor">
            <strong>📝 Editor</strong>
            <span class="status-badge status-done">Complete ✓</span><br/>
            <span class="time-badge">⏱️ {format_duration(editor_data.duration_seconds if editor_data else 0)}</span>
            <span class="token-badge">🔢 {format_tokens(editor_data.total_tokens if editor_data else 0)} tokens</span>
        </div>
        """, unsafe_allow_html=True)
        progress_bar.progress(100)
        
        status_text.text("✅ All agents complete!")
        
        # Summary metrics
        with metrics_container:
            st.subheader("📊 Summary Metrics")
            m_cols = st.columns(5)
            
            with m_cols[0]:
                st.metric("Total Duration", format_duration(telemetry.total_duration_seconds))
            with m_cols[1]:
                st.metric("Total Tokens", f"{telemetry.total_tokens:,}")
            with m_cols[2]:
                st.metric("Input Tokens", f"{telemetry.total_input_tokens:,}")
            with m_cols[3]:
                st.metric("Output Tokens", f"{telemetry.total_output_tokens:,}")
            with m_cols[4]:
                st.metric("Est. Cost", format_cost(telemetry.estimated_cost_usd))
        
        # Final output
        with output_container:
            st.subheader("📄 Final Output")
            st.markdown(f"""
            <div class="output-box">
            {result.output}
            </div>
            """, unsafe_allow_html=True)
        
        # Individual agent outputs
        if show_agent_outputs and result.task_outputs:
            with st.expander("👥 Individual Agent Outputs", expanded=True):
                for agent_name, output in result.task_outputs.items():
                    icon = "🔍" if agent_name == "Researcher" else "✍️" if agent_name == "Writer" else "📝"
                    agent_telem = next((a for a in telemetry.agents if a.agent_name == agent_name), None)
                    
                    st.markdown(f"**{icon} {agent_name}**")
                    if agent_telem:
                        cols = st.columns(4)
                        cols[0].caption(f"⏱️ {format_duration(agent_telem.duration_seconds)}")
                        cols[1].caption(f"🔢 {agent_telem.total_tokens:,} tokens")
                        cols[2].caption(f"📥 {agent_telem.input_tokens:,} in")
                        cols[3].caption(f"📤 {agent_telem.output_tokens:,} out")
                    
                    st.markdown(f"""
                    <div class="agent-output-box">
                    {output[:1500]}{'...' if len(output) > 1500 else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    st.divider()
        
        # Detailed telemetry
        if show_telemetry_details:
            with st.expander("🔬 Detailed Telemetry", expanded=False):
                
                # Visual charts section
                st.markdown("### 📊 Visual Breakdown")
                
                # Prepare data for charts
                agent_names = [a.agent_name for a in telemetry.agents]
                durations = [a.duration_seconds for a in telemetry.agents]
                input_tokens = [a.input_tokens for a in telemetry.agents]
                output_tokens = [a.output_tokens for a in telemetry.agents]
                total_tokens = [a.total_tokens for a in telemetry.agents]
                
                # Duration chart
                st.markdown("**⏱️ Duration by Agent (seconds)**")
                duration_data = {
                    "Agent": agent_names,
                    "Duration (s)": durations
                }
                st.bar_chart(duration_data, x="Agent", y="Duration (s)", color="#FF6B35", horizontal=False)
                
                # Token comparison chart
                st.markdown("**🔢 Token Usage by Agent**")
                token_data = {
                    "Agent": agent_names + agent_names,
                    "Tokens": input_tokens + output_tokens,
                    "Type": ["Input"] * 3 + ["Output"] * 3
                }
                
                # Create side-by-side columns for token breakdown
                tok_cols = st.columns(3)
                colors = ["#0066CC", "#28A745", "#9933CC"]
                for i, agent in enumerate(telemetry.agents):
                    with tok_cols[i]:
                        st.markdown(f"**{agent.agent_name}**")
                        st.metric("Input", f"{agent.input_tokens:,}")
                        st.metric("Output", f"{agent.output_tokens:,}")
                        st.metric("Total", f"{agent.total_tokens:,}")
                
                # Total summary bar
                st.markdown("**📈 Total Token Distribution**")
                total_data = {
                    "Agent": agent_names,
                    "Tokens": total_tokens
                }
                st.bar_chart(total_data, x="Agent", y="Tokens", color="#1E3A5F")
                
                st.divider()
                
                # Raw JSON data
                st.markdown("### 📋 Raw Telemetry Data")
                
                # Format as JSON-like display
                telem_data = {
                    "summary": {
                        "provider": telemetry.provider,
                        "model": telemetry.model,
                        "total_duration_seconds": round(telemetry.total_duration_seconds, 2),
                        "total_tokens": telemetry.total_tokens,
                        "total_input_tokens": telemetry.total_input_tokens,
                        "total_output_tokens": telemetry.total_output_tokens,
                        "total_api_calls": telemetry.total_api_calls,
                        "estimated_cost_usd": round(telemetry.estimated_cost_usd, 6)
                    },
                    "agents": []
                }
                
                for agent in telemetry.agents:
                    telem_data["agents"].append({
                        "name": agent.agent_name,
                        "role": agent.role,
                        "duration_seconds": round(agent.duration_seconds, 2),
                        "input_tokens": agent.input_tokens,
                        "output_tokens": agent.output_tokens,
                        "total_tokens": agent.total_tokens,
                        "api_calls": agent.api_calls,
                        "status": agent.status
                    })
                
                st.json(telem_data)
                
                # Cost breakdown
                if telemetry.provider == "openai":
                    st.markdown("### 💰 Cost Breakdown")
                    config = PROVIDER_CONFIGS["openai"]
                    input_cost = (telemetry.total_input_tokens / 1000) * config.cost_per_1k_input_tokens
                    output_cost = (telemetry.total_output_tokens / 1000) * config.cost_per_1k_output_tokens
                    
                    cost_df = {
                        "Category": ["Input Tokens", "Output Tokens", "Total"],
                        "Tokens": [telemetry.total_input_tokens, telemetry.total_output_tokens, telemetry.total_tokens],
                        "Rate (per 1K)": [f"${config.cost_per_1k_input_tokens}", f"${config.cost_per_1k_output_tokens}", "-"],
                        "Cost": [f"${input_cost:.6f}", f"${output_cost:.6f}", f"${telemetry.estimated_cost_usd:.6f}"]
                    }
                    st.table(cost_df)
    
    elif result.success:
        # Success but no telemetry
        progress_bar.progress(100)
        status_text.text("✅ Complete!")
        
        with output_container:
            st.subheader("📄 Final Output")
            st.markdown(f"""
            <div class="output-box">
            {result.output}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Error
        progress_bar.progress(0)
        status_text.text("❌ Error occurred")
        st.error(f"**Error:** {result.error}")


# =============================================================================
# FOOTER
# =============================================================================

st.divider()
st.caption("""
**MIT Professional Education: Agentic AI** | Module 2: Multi-Agent Systems

This demo uses [CrewAI](https://github.com/joaomdmoura/crewAI) for agent orchestration.
Telemetry values are estimates based on token counting.
""")
