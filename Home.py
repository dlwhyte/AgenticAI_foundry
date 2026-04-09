"""
AgenticAI Foundry - Course Hub Home Page
MIT Professional Education: Applied Generative AI for Digital Transformation
"""

import streamlit as st

st.set_page_config(
    page_title="AgenticAI Foundry",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
  .main-header {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1E3A5F;
    margin-bottom: 0.5rem;
  }
  .sub-header {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 2rem;
  }
  .highlight-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
  }
  .module-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #0066cc;
  }
  .module-card.no-key {
    border-left-color: #28a745;
  }
  .module-card.optional-key {
    border-left-color: #fd7e14;
  }
  .badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-left: 0.5rem;
  }
  .badge-green { background: #d4edda; color: #155724; }
  .badge-orange { background: #fff3cd; color: #856404; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🤖 AgenticAI Foundry</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">MIT Professional Education: Applied Generative AI for Digital Transformation</p>', unsafe_allow_html=True)

# Intro box
st.markdown("""
<div class="highlight-box">
<h3>🎯 What You Will Build</h3>
<p style="font-size: 1.1rem; margin-bottom: 0;">
Move beyond chatting with AI — learn how to build <strong>AI systems that take action</strong>.
This course covers the economics of model choice, multi-agent orchestration, tool integration via MCP,
security guardrails, and keeping humans in the loop.
</p>
</div>
""", unsafe_allow_html=True)

# Prerequisite callout
st.info("""
📚 **New to Generative AI?** Start with [GenAI Foundry](https://github.com/dlwhyte/GenAI_foundry)
to learn LLMs, RAG, and prompt engineering before diving into agents.
""")

# Module table
st.markdown("---")
st.markdown("### 🗺️ Course Modules")
st.markdown("Use the **sidebar** to navigate between modules. Here is what each one covers:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="module-card no-key">
<h4>💰 Module 1 — LLM Cost Explorer
<span class="badge badge-green">No API Key</span></h4>
<p>Why the same AI task can cost $1 or $230 depending on model choice.
Explore token economics, scale projections, and cost comparisons across 10+ models.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="module-card optional-key">
<h4>🔗 Module 2b — LangChain Agent Demo
<span class="badge badge-orange">API Key Optional</span></h4>
<p>How a single agent uses tools (web search, calculators) to answer questions in real time using the ReAct loop.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="module-card no-key">
<h4>🛡️ Module 4 — Agent Security Demo
<span class="badge badge-green">Demo: No Key</span></h4>
<p>Prompt injection attacks and defence-in-depth guardrails. See how malicious inputs try to hijack agents and how to stop them.</p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="module-card optional-key">
<h4>🤖 Module 2a — Multi-Agent Demo
<span class="badge badge-orange">API Key Optional</span></h4>
<p>How three AI agents collaborate like a team using CrewAI. Roles, tasks, and orchestration — see the Observe→Think→Act loop at scale.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="module-card no-key">
<h4>🔌 Module 3 — MCP Explorer
<span class="badge badge-green">No API Key</span></h4>
<p>How AI agents connect to external tools — calendars, CRMs, databases — via the Model Context Protocol (MCP).</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="module-card no-key">
<h4>🧑‍✈️ Module 5 — Human-in-the-Loop (HITL)
<span class="badge badge-green">No API Key</span></h4>
<p>Three patterns for keeping humans in control: approval gates, confidence thresholds, and audit trails. Essential for production agentic systems.</p>
</div>
""", unsafe_allow_html=True)

# Quick start
st.markdown("---")
st.markdown("### 🚀 Quick Start")

col1, col2, col3 = st.columns(3)
with col1:
    st.success("**Step 1 — No setup needed**\n\nModules 1, 3, 4, and 5 work immediately. Click any module in the sidebar.")
with col2:
    st.warning("**Step 2 — Optional: Add AI**\n\nFor Module 2, install Ollama (free) or add an OpenAI API key in the sidebar.")
with col3:
    st.info("**Step 3 — Explore**\n\nWork through modules in order, or jump to what interests you most.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
<p>MIT Professional Education: Applied Generative AI for Digital Transformation</p>
<p>Modules 1, 3, 4 &amp; 5 work immediately — no API key required &nbsp;·&nbsp; Module 2 requires Ollama or OpenAI</p>
</div>
""", unsafe_allow_html=True)
