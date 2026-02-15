# AgenticAI Foundry 🤖

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MIT Professional Education: Applied Generative AI for Digital Transformation**

*Interactive demos for understanding AI economics, multi-agent systems, agent integration, and AI security*

---

## 🎯 What's Included

| Demo | Module | Description | API Key? |
|------|--------|-------------|----------|
| **💰 LLM Cost Explorer** | Module 1 | Calculate and compare LLM API costs across providers | No |
| **🤖 Multi-Agent Demo** | Module 2 | Watch three AI agents collaborate (CrewAI) | Optional |
| **🔗 LangChain Agent Demo** | Module 2 | Single agent with web search tool (LangChain) | Optional |
| **🔌 MCP Explorer** | Module 3 | Understand the Model Context Protocol — how AI agents connect to tools | No |
| **🛡️ Agent Security Demo** | Module 3 | Prompt injection attacks & defense-in-depth guardrails | Demo: No / Live: Optional |

> More demos will be added as the course progresses.

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/dlwhyte/AgenticAI_foundry.git
cd AgenticAI_foundry

# Build and run
docker build -t agenticai-foundry .
docker run -p 8501:8501 agenticai-foundry
```

Open [http://localhost:8501](http://localhost:8501)

### Option 2: Python

```bash
# Clone and install
git clone https://github.com/dlwhyte/AgenticAI_foundry.git
cd AgenticAI_foundry
pip install -r requirements.txt

# Run
streamlit run Home.py
```

---

## ✨ Demo Details

### 💰 LLM Cost Explorer (Module 1)

> **The same AI transaction can cost between $1 and $230** — a 200x variance!

- **Real-time Token Counter** — Uses OpenAI's tiktoken
- **Multi-Model Comparison** — 10+ models from OpenAI, Anthropic, Google
- **Scale Analysis** — See costs from 1K to 1M API calls
- **Export Results** — CSV, JSON for assignments

**Assignment:** Use this to analyze model pricing at scale for your write-up.

### 🤖 Multi-Agent Demo (Module 2)

> Watch three agents collaborate: **Researcher → Writer → Editor**

- **Three Collaborating Agents** — Sequential task handoff via CrewAI
- **Dual Provider Support** — Ollama (free, local) or OpenAI (paid, cloud)
- **Live Agent Activity** — Watch agents hand off work in real-time
- **CLI Support** — Run from command line or Streamlit

**Assignment:** Observe agent specialization, telemetry, and collaboration patterns.

### 🔗 LangChain Agent Demo (Module 2)

> Single agent with tools: **Think → Search → Answer**

- **Single Agent + Tools** — Contrast with CrewAI's multi-agent approach
- **Real-Time Web Search** — Get current crypto prices via DuckDuckGo
- **ReAct Pattern** — Watch the agent think, act, and observe
- **Same Provider Options** — Works with Ollama or OpenAI

**Assignment:** Compare single-agent vs multi-agent patterns.

### 🔌 MCP Explorer (Module 3)

> MCP is **USB-C for AI** — one standard protocol connecting agents to any tool.

- **Step-by-Step Scenarios** — Walk through real MCP interactions (calendar, Spotify, Salesforce, DevOps)
- **Protocol Messages** — See the actual JSON-RPC requests and responses
- **MCP vs Alternatives** — Side-by-side comparison with Zapier and custom APIs
- **Integration Framework** — Understand when to use which approach

**Assignment:** Supports Q3 (integration), Q4 (safety), and the overall proposal design.
No API key required — this is an educational simulation tool.

### 🛡️ Agent Security Demo (Module 3)

> No single guardrail catches every attack — AI security requires **defense in depth**.

- **Six Attack Scenarios** — Direct injection, role-playing (DAN), gradual escalation, system prompt extraction, policy bypass, indirect injection
- **Five Defense Layers** — Input validation, scope enforcement, constitutional AI review, output filtering, human-in-the-loop
- **Interactive Testing** — Toggle guardrails on/off, test them individually, see the coverage matrix
- **Business Impact Calculator** — Breach costs vs. guardrail ROI by industry (Healthcare, Finance, Retail, Tech)
- **Real-World Cases** — Knight Capital ($440M), Rogers outage, Optus outage

**Two modes:**
- **Demo Mode** — Pre-built scenarios, no API key needed
- **Live Mode** — Send real prompts to OpenAI, Anthropic, or Ollama with guardrails you control

**Assignment:** Supports Q4 (safety & guardrails), Q5 (rollout), Q6 (risks & mitigation).

---

## 🤖 Multi-Agent Demo Setup

The Multi-Agent and LangChain demos need an AI "brain." You have two options:

### What is Ollama?

**Ollama** lets you run powerful AI models **locally on your own computer** — for free, with no data leaving your machine.

| Feature | Ollama (Local) | OpenAI (Cloud) |
|---------|----------------|----------------|
| **Cost** | Free | ~$0.01/run |
| **Privacy** | Data stays local | Data sent to cloud |
| **Speed** | Depends on your hardware | Consistently fast |
| **Internet** | Not required | Required |
| **Setup** | Install + download model | Just need API key |

### Option A: Ollama (Free, Local) — Recommended for Learning

```bash
# 1. Install Ollama
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
# Windows: Download from https://ollama.ai

# 2. Download an AI model (2 GB, takes 2-5 min)
ollama pull llama3.2

# 3. Start the Ollama server (keep this running)
ollama serve

# 4. Install Python dependencies (if running outside Docker)
pip install -r requirements-crewai.txt
```

### Option B: OpenAI (Paid, Cloud) — Faster Results

```bash
# 1. Get an API key from platform.openai.com

# 2. Set it in your environment
export OPENAI_API_KEY="sk-your-key-here"

# 3. Install Python dependencies (if running outside Docker)
pip install -r requirements-crewai.txt
```

---

## 📚 Documentation

| Guide | Best For | What It Covers |
|-------|----------|----------------|
| **[Beginner's Guide](docs/BEGINNERS_GUIDE.md)** | Absolute beginners | Full explanations of every technology, step-by-step setup, glossary |
| **[LLM Cost Guide](docs/LLM_COST_GUIDE.md)** | Module 1 | Token economics, model selection, cost drivers |
| **[Multi-Agent Guide](docs/MULTI_AGENT_GUIDE.md)** | Module 2 | CrewAI vs LangChain, single-agent vs multi-agent patterns |
| **[MCP Guide](docs/MCP_GUIDE.md)** | Module 3 | Understanding the Model Context Protocol |
| **[Security Demo Guide](docs/SECURITY_DEMO_GUIDE.md)** | Module 3 | Prompt injection attacks, guardrails, business case |
| **[CrewAI Setup](docs/CREWAI_SETUP.md)** | Quick reference | Commands, troubleshooting, CLI usage |
| **[Docker Guide](docs/DOCKER_GUIDE.md)** | Container users | Docker-specific setup |

**New to AI agents?** Start with the [Beginner's Guide](docs/BEGINNERS_GUIDE.md) — it explains everything from scratch.

---

## 📁 Project Structure

```
AgenticAI_foundry/
├── Home.py                         # Landing page — course hub
├── pages/
│   ├── 1_LLM_Cost_Calculator.py    # Cost calculator (Module 1)
│   ├── 2_Multi_Agent_Demo.py       # CrewAI multi-agent demo (Module 2)
│   ├── 3_LangChain_Agent_Demo.py   # LangChain tool agent (Module 2)
│   ├── 4_MCP_Explorer.py           # MCP protocol explorer (Module 3)
│   └── 5_Agent_Security_Demo.py    # Prompt injection & guardrails (Module 3)
├── crews/                          # 🧠 CrewAI multi-agent logic
│   ├── __init__.py
│   └── research_crew.py            # Agent definitions & orchestration
├── agents/                         # 🔗 LangChain single-agent logic
│   ├── __init__.py
│   └── crypto_agent.py             # Web search agent for crypto prices
├── docs/
│   ├── BEGINNERS_GUIDE.md          # Comprehensive beginner tutorial
│   ├── LLM_COST_GUIDE.md           # Module 1: Token economics & cost analysis
│   ├── MULTI_AGENT_GUIDE.md        # Module 2: CrewAI vs LangChain patterns
│   ├── MCP_GUIDE.md                # Module 3: Model Context Protocol
│   ├── SECURITY_DEMO_GUIDE.md      # Module 3: Prompt injection & guardrails
│   ├── CREWAI_SETUP.md             # Quick setup reference
│   └── DOCKER_GUIDE.md             # Docker setup guide
├── Dockerfile
├── requirements.txt                # Base Streamlit dependencies
├── requirements-crewai.txt         # CrewAI + LangChain dependencies
└── README.md
```

---

## 📊 Module Connections

### Module 1: LLM Cost Explorer

> **The same AI transaction can cost between $1 and $230** — a 200x variance!

Use this tool to understand token economics and model pricing before scaling AI in your org.

### Module 2: Multi-Agent Systems

> Watch agents collaborate: **Researcher → Writer → Editor**

See multi-agent orchestration (CrewAI) and single-agent reasoning (LangChain) side by side.

#### CrewAI vs LangChain — Two Approaches

| Aspect | CrewAI (Multi-Agent) | LangChain (Tool Agent) |
|--------|---------------------|------------------------|
| **Metaphor** | Team of employees | Single agent with tools |
| **Pattern** | Sequential handoff | ReAct (Reason + Act) |
| **Example** | Research → Write → Edit | Question → Search → Answer |
| **Best For** | Complex workflows | Real-time data retrieval |

#### How CrewAI Specializes Agents

```python
Agent(
    role="Research Analyst",             # Job title
    goal="Gather info about {topic}",    # What to achieve
    backstory="You are an experienced    # Shapes behavior
               researcher with expertise..."
    llm=llm
)
```

CrewAI combines these attributes with task instructions to construct prompts sent to the LLM. See `crews/research_crew.py` for the full implementation.

### Module 3: Agent Security & Integration

> MCP is **USB-C for AI** — and guardrails are the **safety net underneath**.

Two demos cover Module 3:

**MCP Explorer** — How agents connect to tools via a standardized protocol. Compares MCP vs. Zapier vs. custom APIs across real scenarios (calendar scheduling, CRM lookup, DevOps triage).

**Agent Security Demo** — How agents can be attacked via prompt injection and how to defend them with layered guardrails. Covers six attack types, five defense layers, and the business case for investing in AI security.

#### MCP vs Other Approaches

| Aspect | Zapier / n8n | Custom APIs | MCP |
|--------|-------------|-------------|-----|
| **Complexity** | Low (no-code) | High (custom dev) | Medium (standard) |
| **AI Awareness** | None — trigger/action | Manual integration | Native AI support |
| **Context / Memory** | No | Build it yourself | Built-in |
| **Best For** | Simple automations | Unique business logic | AI agent ecosystems |

#### Defense in Depth

| Layer | What It Does | Cost | Catches |
|-------|-------------|------|---------|
| 🔍 Input Validation | Keyword/pattern scan of user input | ~5ms, free | Known attack patterns |
| 🎯 Scope Enforcement | Whitelist of allowed agent actions | ~5ms, free | Privilege escalation |
| 🧠 Constitutional Review | Second LLM reviews draft response | ~1–2s, 2× API cost | Subtle, creative attacks |
| 🔒 Output Filtering | Scan response for PII/secrets | ~10ms, free | Data leaks |
| 👤 Human-in-the-Loop | Human approves high-risk actions | Minutes | Financial/irreversible actions |

---

## 🖥️ CLI Usage

The Multi-Agent Demo also works from the command line:

```bash
# With Ollama (free)
python -m crews.research_crew --provider ollama --task "Research AI in healthcare"

# With OpenAI
python -m crews.research_crew --provider openai --task "Research AI in healthcare"

# Check your setup
python -m crews.research_crew --check
```

---

## 🛠️ Technologies

| Technology | What It Does | Learn More |
|------------|--------------|------------|
| **[Streamlit](https://streamlit.io/)** | Web app framework | Creates the UI |
| **[CrewAI](https://github.com/joaomdmoura/crewAI)** | Multi-agent orchestration | Coordinates agents |
| **[Ollama](https://ollama.ai/)** | Local LLM runtime | Runs AI on your machine |
| **[LangChain](https://langchain.com/)** | LLM integrations | Connects to AI providers |
| **[Plotly](https://plotly.com/)** | Interactive charts | Visualizes cost data |
| **[Docker](https://www.docker.com/)** | Containerization | Easy deployment |

---

## ❓ Troubleshooting

### Quick Fixes

| Problem | Solution |
|---------|----------|
| "Ollama not running" | Run `ollama serve` in a terminal |
| "Model not found" | Run `ollama pull llama3.2` |
| "Out of memory" | Try smaller model: `ollama pull phi3` |
| "Slow responses" | Normal for local AI; try OpenAI for speed |
| "Import errors" | Run `pip install crewai langchain-community` |

For detailed troubleshooting, see [Beginner's Guide — Troubleshooting](docs/BEGINNERS_GUIDE.md#troubleshooting-for-beginners).

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

<p align="center">
  <b>MIT Professional Education | Applied Generative AI for Digital Transformation</b><br>
  <i>Demos work locally — API keys optional (Ollama mode)</i>
</p>
