"""
    AgenticAI Foundry – Home Page
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
        "doc_url": "https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/LLM_COST_GUIDE.md",
        "doc_label": "LLM Cost Guide",
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
        "doc_url": "https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/MULTI_AGENT_GUIDE.md",
        "doc_label": "Multi-Agent Guide",
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
        "doc_url": "https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/MULTI_AGENT_GUIDE.md",
        "doc_label": "Multi-Agent Guide",
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
        "doc_url": "https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/MCP_GUIDE.md",
        "doc_label": "MCP Guide",
    },
    {
        "module": 3,
        "icon": "🛡️",
        "title": "Agent Security Demo",
        "page": "Agent Security Demo",
        "tagline": "No single guardrail catches every attack — AI security requires **defense in depth**.",
        "learns": [
            "Six prompt injection attack types (direct, role-play, indirect, escalation)",
            "Five defense layers: input filters → constitutional AI → human-in-the-loop",
            "Toggle guardrails on/off and see what gets caught in real time",
            "Business case: breach costs vs. guardrail ROI by industry",
        ],
        "assignment": "Assignment 3 — Q4: Safety measures, Q5: Rollout, Q6: Risks",
        "api_required": "Demo Mode free; Live Mode needs OpenAI/Ollama",
        "doc_url": "https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/SECURITY_DEMO_GUIDE.md",
        "doc_label": "Security Demo Guide",
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
    .api-no  { background: #F0FFF4; color: #2F855A; }
    .api-opt { background: #FFF3D6; color: #975A16; }
    .api-yes { background: #FFF5F5; color: #C53030; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown('<p class="main-header">🤖 AgenticAI Foundry</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">MIT Professional Education — Applied Generative AI for Digital Transformation</p>', unsafe_allow_html=True)

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

        doc_html = ""
        if d.get("doc_url"):
            doc_html = f'<p style="font-size: 0.85rem; margin-top: 0.3rem;"><a href="{d["doc_url"]}" target="_blank">📖 Read the {d["doc_label"]}</a></p>'

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
            {doc_html}
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
- **Module 3?** Walk through the **MCP Explorer** and **Agent Security Demo** — Demo Mode needs no setup.
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
| **[Security Demo Guide](https://github.com/dlwhyte/AgenticAI_foundry/blob/main/docs/SECURITY_DEMO_GUIDE.md)** | Module 3 | Prompt injection attacks, guardrails, business case |

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
