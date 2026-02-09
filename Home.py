"""
AgenticAI Foundry - Home Page
MIT Professional Education: Applied Generative AI for Digital Transformation
"""

import streamlit as st

st.set_page_config(
    page_title="AgenticAI Foundry",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DEMO REGISTRY — Add new demos here
# ─────────────────────────────────────────────
# Each entry becomes a card on the landing page.
# To add a Module 4/5/6 demo, just append to this list.

DEMOS = [
    {
        "module": 1,
        "icon": "💰",
        "title": "LLM Cost Explorer",
        "page": "LLM Cost Calculator",
        "tagline": "The same AI transaction can cost between **$1 and $230** — a 200x variance.",
        "learns": [
            "Real-time token counting with tiktoken",
            "Compare 10+ models across OpenAI, Anthropic, Google",
            "Project costs from 1K to 1M API calls",
            "Export CSV/JSON for your assignment",
        ],
        "assignment": "Assignment 1 — Analyze model pricing at scale",
        "api_required": False,
    },
    {
        "module": 2,
        "icon": "🤖",
        "title": "Multi-Agent Demo",
        "page": "Multi Agent Demo",
        "tagline": "Watch three AI agents collaborate: **Researcher → Writer → Editor**.",
        "learns": [
            "CrewAI multi-agent orchestration",
            "Agent specialization via role, goal, backstory",
            "Sequential task handoff between agents",
            "Ollama (free/local) or OpenAI (cloud)",
        ],
        "assignment": "Assignment 2 — Observe agent collaboration and telemetry",
        "api_required": "Optional (works with free Ollama)",
    },
    {
        "module": 2,
        "icon": "🔗",
        "title": "LangChain Agent Demo",
        "page": "LangChain Agent Demo",
        "tagline": "Single agent with tools: **Think → Search → Answer** in real time.",
        "learns": [
            "LangChain tool-augmented reasoning",
            "ReAct pattern (Reason + Act + Observe)",
            "Real-time web search via DuckDuckGo",
            "Contrast with CrewAI's multi-agent approach",
        ],
        "assignment": "Assignment 2 — Compare single-agent vs multi-agent patterns",
        "api_required": "Optional (works with free Ollama)",
    },
    {
        "module": 3,
        "icon": "🔌",
        "title": "MCP Explorer",
        "page": "MCP Explorer",
        "tagline": "MCP is **USB-C for AI** — one standard protocol connecting agents to any tool.",
        "learns": [
            "Step-by-step MCP interaction walkthroughs",
            "Real JSON-RPC protocol messages",
            "Side-by-side: MCP vs Zapier vs Custom APIs",
            "When to use which integration approach",
        ],
        "assignment": "Assignment 3 — Q3: How would your agent integrate with existing systems?",
        "api_required": False,
    },
]

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.15rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .hero-box {
        background: linear-gradient(135deg, #0F2B46 0%, #1C7293 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0 1.5rem 0;
    }
    .module-badge {
        display: inline-block;
        background: #E8A838;
        color: #1E3A5F;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        margin-bottom: 0.3rem;
    }
    .demo-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.3rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1C7293;
        min-height: 320px;
    }
    .demo-card h4 {
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
        color: #1E3A5F;
    }
    .api-badge {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.15rem 0.5rem;
        border-radius: 8px;
        margin-top: 0.3rem;
    }
    .api-no { background: #F0FFF4; color: #2F855A; }
    .api-opt { background: #FFF3D6; color: #975A16; }
    .api-yes { background: #FFF5F5; color: #C53030; }
    .stat-number {
        font-size: 2.2rem;
        font-weight: bold;
        color: #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown('<p class="main-header">🤖 AgenticAI Foundry</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">MIT Professional Education — Applied Generative AI for Digital Transformation</p>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <h4 style="margin-top:0; color: #E8A838;">Hands-On Demos for Every Module</h4>
    <p style="font-size: 1.05rem; margin-bottom: 0;">
    This app contains interactive tools that bring course concepts to life — from token economics 
    to multi-agent orchestration to protocol-level integration. Each demo connects directly to an 
    assignment so you can <strong>learn by doing</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATS ROW
# ─────────────────────────────────────────────

modules_covered = sorted(set(d["module"] for d in DEMOS))
module_str = ", ".join(str(m) for m in modules_covered)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.8rem; background: #f0f7ff; border-radius: 10px;">
    <p class="stat-number">{len(DEMOS)}</p>
    <p><strong>Interactive Demos</strong><br/>Hands-on tools you can run right now</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.8rem; background: #f0f7ff; border-radius: 10px;">
    <p class="stat-number">{len(modules_covered)}</p>
    <p><strong>Modules Covered</strong><br/>Modules {module_str}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    no_key = sum(1 for d in DEMOS if d["api_required"] is False)
    st.markdown(f"""
    <div style="text-align: center; padding: 0.8rem; background: #f0f7ff; border-radius: 10px;">
    <p class="stat-number">{no_key}</p>
    <p><strong>No API Key Needed</strong><br/>Start exploring immediately</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DEMO CARDS
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("### 🎓 Explore the Demos")

for i in range(0, len(DEMOS), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx >= len(DEMOS):
            break
        d = DEMOS[idx]

        if d["api_required"] is False:
            api_html = '<span class="api-badge api-no">✅ No API key needed</span>'
        elif d["api_required"] is True:
            api_html = '<span class="api-badge api-yes">🔑 API key required</span>'
        else:
            api_html = f'<span class="api-badge api-opt">🔑 {d["api_required"]}</span>'

        learns_html = "".join(f"<li>{item}</li>" for item in d["learns"])

        with col:
            st.markdown(f"""
            <div class="demo-card">
                <span class="module-badge">MODULE {d['module']}</span>
                <h4>{d['icon']} {d['title']}</h4>
                <p>{d['tagline']}</p>
                <ul style="font-size: 0.9rem; color: #4a5568; margin: 0.5rem 0;">
                    {learns_html}
                </ul>
                <p style="font-size: 0.85rem; color: #065A82;"><strong>📝 {d['assignment']}</strong></p>
                {api_html}
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GETTING STARTED
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("### 🚀 Getting Started")

st.info("""
👈 **Select a demo from the sidebar** to begin exploring.

- **Module 1?** Start with the **LLM Cost Explorer** — no setup needed.
- **Module 2?** Try the **Multi-Agent Demo** with Ollama (free) or OpenAI.
- **Module 3?** Walk through the **MCP Explorer** — no setup needed.
""")

# ─────────────────────────────────────────────
# QUICK REFERENCE
# ─────────────────────────────────────────────

with st.expander("📚 Documentation & Setup Guides"):
    st.markdown("""
    | Guide | Best For | What It Covers |
    |-------|----------|----------------|
    | **[Beginner's Guide](https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/BEGINNERS_GUIDE.md)** | Absolute beginners | Full explanations of every technology, step-by-step setup |
    | **[CrewAI Setup](https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/CREWAI_SETUP.md)** | Quick reference | Commands, troubleshooting, CLI usage |
    | **[Docker Guide](https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/DOCKER_GUIDE.md)** | Container users | Docker-specific setup and troubleshooting |
    | **[MCP Guide](https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/MCP_GUIDE.md)** | Module 3 | Understanding the Model Context Protocol |
    
    **New to all of this?** Start with the [Beginner's Guide](https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/BEGINNERS_GUIDE.md) — it explains everything from scratch.
    """)

with st.expander("⚡ Quick Start Commands"):
    st.markdown("""
    **Docker (recommended):**
    ```bash
    git clone https://github.com/dlwhyte/AgenticAI_foundry.git
    cd AgenticAI_foundry
    docker build -t agenticai-foundry .
    docker run -p 8501:8501 agenticai-foundry
    ```
    
    **Python (no Docker):**
    ```bash
    git clone https://github.com/dlwhyte/AgenticAI_foundry.git
    cd AgenticAI_foundry
    pip install -r requirements.txt
    streamlit run Home.py
    ```
    
    Then open [http://localhost:8501](http://localhost:8501)
    """)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
<p><strong>MIT Professional Education | Applied Generative AI for Digital Transformation</strong></p>
<p>Demos work locally — API keys optional (Ollama mode available)</p>
</div>
""", unsafe_allow_html=True)
