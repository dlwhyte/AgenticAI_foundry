# Agentic AI Foundry 🤖

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MIT Professional Education: Agentic AI**  
*Interactive demos for understanding AI economics and multi-agent systems*

---

## 🎯 What's Included

| Demo | Module | Description |
|------|--------|-------------|
| **💰 LLM Cost Explorer** | Module 1 | Calculate and compare LLM API costs across providers |
| **🤖 Multi-Agent Demo** | Module 2 | Watch three AI agents collaborate in real-time |

---

## ✨ Features

### 💰 LLM Cost Explorer (Module 1)
- **Real-time Token Counter** — Uses OpenAI's tiktoken
- **Multi-Model Comparison** — 10+ models from OpenAI, Anthropic, Google
- **Scale Analysis** — See costs from 1K to 1M API calls
- **Export Results** — CSV, JSON for assignments

### 🤖 Multi-Agent Demo (Module 2)
- **Three Collaborating Agents** — Researcher → Writer → Editor
- **Dual Provider Support** — Ollama (free, local) or OpenAI (paid, cloud)
- **Live Agent Activity** — Watch agents hand off work in real-time
- **CLI Support** — Run from command line or Streamlit

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

## 🤖 Multi-Agent Demo Setup

The Multi-Agent Demo lets you watch AI agents collaborate. You have two options for the AI "brain":

### What is Ollama?

**Ollama** lets you run powerful AI models **locally on your own computer** — for free, with no data leaving your machine. It's like having ChatGPT on your laptop, but you own it.

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
# macOS:
brew install ollama
# Linux:
curl -fsSL https://ollama.ai/install.sh | sh
# Windows: Download from https://ollama.ai

# 2. Download an AI model (4.7 GB, takes 2-5 min)
ollama pull llama3.2

# 3. Start the Ollama server (keep this running)
ollama serve

# 4. Install Python dependencies (in new terminal)
pip install crewai langchain-community
```

### Option B: OpenAI (Paid, Cloud) — Faster Results

```bash
# 1. Get an API key from platform.openai.com
# 2. Set it in your environment
export OPENAI_API_KEY="sk-your-key-here"

# 3. Install Python dependencies
pip install crewai langchain-openai
```

---

## 📚 Documentation

| Guide | For Who | What It Covers |
|-------|---------|----------------|
| **[Beginner's Guide](docs/BEGINNERS_GUIDE.md)** | Absolute beginners | Full explanations of every technology, step-by-step setup, glossary |
| **[CrewAI Setup](docs/CREWAI_SETUP.md)** | Quick reference | Commands, troubleshooting, CLI usage |
| **[Docker Guide](docs/DOCKER_GUIDE.md)** | Container users | Docker-specific setup |

**New to AI agents?** Start with the [Beginner's Guide](docs/BEGINNERS_GUIDE.md) — it explains everything from scratch.

---

## 📁 Project Structure

```
AgenticAI_foundry/
├── Home.py                        # Landing page
├── pages/
│   ├── 1_LLM_Cost_Calculator.py   # Cost calculator (Module 1)
│   └── 2_Multi_Agent_Demo.py      # Multi-agent demo (Module 2)
├── crews/
│   ├── __init__.py
│   └── research_crew.py           # Agent logic (CLI + importable)
├── docs/
│   ├── BEGINNERS_GUIDE.md         # Comprehensive beginner tutorial
│   ├── CREWAI_SETUP.md            # Quick setup reference
│   └── DOCKER_GUIDE.md            # Docker setup guide
├── Dockerfile
├── requirements.txt
└── README.md
```

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

## 📊 Module Connections

### Module 1: LLM Cost Explorer
> **The same AI transaction can cost between $1 and $230** — a 200x variance!

Use this tool to understand token economics and model pricing.

### Module 2: Multi-Agent Demo
> Watch three agents collaborate: **Researcher → Writer → Editor**

See multi-agent orchestration in action with CrewAI.

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

For detailed troubleshooting, see [Beginner's Guide - Troubleshooting](docs/BEGINNERS_GUIDE.md#troubleshooting-for-beginners).

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

<p align="center">
  <b>MIT Professional Education | Agentic AI Course</b><br>
  <i>Demos work locally — API keys optional (Ollama mode)</i>
</p>
