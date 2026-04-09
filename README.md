# AgenticAI Foundry 🤖

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MIT Professional Education: Applied Generative AI for Digital Transformation**
*Interactive demos for understanding AI economics, multi-agent systems, and agent integration*

---
> 📚 **New to Generative AI?** Start with [GenAI Foundry](https://github.com/dlwhyte/GenAI_foundry) to learn LLMs, RAG, and prompt engineering before diving into agents.



## 📥 New Here? Start With This

> **[⬇️ Download the Student Quick Start Guide (PDF)](docs/Student_Quick_Start.pdf)**
>
> The Quick Start Guide walks you through everything with screenshots — how to get the code,
> which setup path to choose, and what you should see when it's working.
> **Download this before doing anything else.**

---

## 🎯 What's Included

| Demo | Module | What You'll Learn | API Key Needed? |
|------|--------|-------------------|-----------------|
| 💰 **LLM Cost Explorer** | Module 1 | Why the same AI task can cost $1 or $230 depending on model choice | No |
| 🤖 **Multi-Agent Demo** | Module 2 | How three AI agents collaborate like a team (CrewAI) | Optional |
| 🔗 **LangChain Agent Demo** | Module 2 | How a single agent uses tools to answer questions in real time | Optional |
| 🔌 **MCP Explorer** | Module 3 | How AI agents connect to external tools (calendars, CRMs, databases) | No |
| 🛡️ **Agent Security Demo** | Module 4 | Prompt injection attacks and defense-in-depth guardrails | Demo: No / Live: Optional |

> Modules 1, 3, and 4 (Demo Mode) work immediately — no account, no API key required.
> Module 2 demos need either Ollama (free, local) or an OpenAI API key.

---

## 🚀 Getting Started — Choose Your Path

**Not sure which path to take? Ask yourself one question:**

> *"Have I used Docker before, or am I comfortable installing a new application from a website?"*

- **Yes →** Take [Path A: Docker](#path-a-docker-recommended) — more reliable, fewer things can go wrong once running
- **No →** Take [Path B: Python](#path-b-python) — more familiar territory if you've used Python before

Both paths give you the full app. Docker is recommended because it handles all the dependencies for you.

---

### Step 0 — Get the Code (Both Paths)

You need a copy of this repository on your computer before doing anything else.

**Option 1: Download ZIP (easiest — no GitHub account needed)**

1. Click the green **`< > Code`** button at the top of this page
2. Click **"Download ZIP"**
3. Find the downloaded file (usually in your Downloads folder)
4. Right-click → **Extract All** (Windows) or double-click (Mac) to unzip it
5. Remember where you saved the folder — you'll need it in the next steps

**Option 2: Clone with Git (if you have Git installed)**

```bash
git clone https://github.com/dlwhyte/AgenticAI_foundry.git
```

---

### Path A: Docker (Recommended)

Docker packages the entire app — Python, all libraries, everything — into a self-contained box.
Once installed, it runs identically on Windows, Mac, and Linux with no dependency conflicts.

**What is Docker?** Think of it like a shipping container for software. Everything the app needs
is packed inside. You don't need to install Python or any libraries separately.

**Time required:** ~20 minutes first time (mostly waiting for downloads). Under 1 minute after that.

#### Step 1 — Install Docker Desktop

- **Windows or Mac:** Download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) and run the installer
- **Linux:** See `docs/DOCKER_GUIDE.md` for Linux-specific instructions

After installing, open **Docker Desktop** and wait for it to fully start (you'll see a whale icon in your taskbar/menu bar stop animating).

> ✅ You'll know Docker is ready when the whale icon is still (not animating).

#### Step 2 — Open a Terminal

| System | How to open a terminal |
|--------|----------------------|
| **Windows** | Press `Win + R`, type `powershell`, press Enter |
| **Mac** | Press `Cmd + Space`, type `Terminal`, press Enter |
| **Linux** | Press `Ctrl + Alt + T` |

#### Step 3 — Navigate to the Project Folder

Type the following, replacing the path with where you saved the folder in Step 0:

```bash
# Windows example (adjust the path to match where you saved it)
cd C:\Users\YourName\Downloads\AgenticAI_foundry

# Mac/Linux example
cd ~/Downloads/AgenticAI_foundry
```

> 💡 **Tip:** You can drag the folder onto the terminal window and it will paste the path for you.

#### Step 4 — Build the App (one-time only)

```bash
docker build -t agenticai-foundry .
```

This downloads Python and all required libraries. It will take 2–5 minutes and show a lot of output — that's normal. Wait until you see:

```
Successfully built xxxxxxxxxx
Successfully tagged agenticai-foundry:latest
```

#### Step 5 — Run the App

```bash
docker run -p 8501:8501 agenticai-foundry
```

You'll see output ending with something like:

```
You can now view your Streamlit app in your browser.
URL: http://localhost:8501
```

#### Step 6 — Open in Your Browser

Open your web browser and go to:

**http://localhost:8501**

🎉 You should see the AgenticAI Foundry home page!

#### Step 7 — Stop the App

When you're done, go back to the terminal and press **`Ctrl + C`**.

#### Troubleshooting Docker

| Problem | Solution |
|---------|----------|
| "Docker command not found" | Make sure Docker Desktop is open and running |
| "Cannot connect to Docker daemon" | Open Docker Desktop and wait for the whale to stop animating |
| "Port 8501 is already in use" | Run `docker run -p 8502:8501 agenticai-foundry` and open `http://localhost:8502` |
| Build seems stuck | Wait — first build downloads ~500MB, can take 5+ minutes on slower connections |

For more detailed Docker troubleshooting, see `docs/DOCKER_GUIDE.md`.

---

### Path B: Python

Run the app directly using Python. You'll have more visibility into the code but there are more
steps that can vary by operating system.

**Time required:** ~15 minutes, more steps involved.

> ⚠️ **Check your Python version before starting.** Open a terminal and run:
> ```
> python3 --version
> ```
> If it shows **Python 3.9 or lower** — stop and use Docker (Path A) instead.
> CrewAI (required for Module 2) only works on Python 3.10 or higher.
> Modules 1 and 3 will still work on Python 3.9, but Module 2 will not.

#### Step 1 — Install Python 3.10 or Higher

Check your version first:

```bash
python3 --version
```

- If you see `Python 3.10`, `3.11`, `3.12`, or `3.13` — skip to Step 2, you're ready
- If you see `Python 3.9` or lower — download a newer version from [python.org/downloads](https://www.python.org/downloads/) and run the installer

> ⚠️ **Windows users:** During installation, check the box that says **"Add Python to PATH"** — this is easy to miss and causes problems later if skipped.
>
> ⚠️ **Mac users:** Your Mac may have Python 3.9 built in (from Xcode). If so, download Python 3.11 from [python.org/downloads](https://www.python.org/downloads/) — it installs alongside the existing version without breaking anything.

#### Step 2 — Open a Terminal and Navigate to the Project Folder

See Step 2 and Step 3 from the Docker path above for how to open a terminal and navigate to the folder.

#### Step 3 — Install the App's Dependencies

> ⚠️ **This step is required — do not skip it.** If you skip this, the app will crash with an error like `ModuleNotFoundError: No module named 'tiktoken'`.

Run both of these commands, one at a time:

```bash
pip3 install -r requirements.txt
pip3 install -r requirements-crewai.txt
```

This downloads all required Python libraries. It will take 2–5 minutes and show a lot of output — that's normal. Wait until you see your terminal prompt again before moving on.

> 💡 If `pip3` gives "command not found", try `pip install -r requirements.txt` instead.

#### Step 4 — Run the App

```bash
python3 -m streamlit run Home.py
```

Your browser should open automatically to `http://localhost:8501`.
If it doesn't, open your browser and go there manually.

#### Step 5 — Stop the App

Press **`Ctrl + C`** in the terminal.

#### Troubleshooting Python

| Problem | Solution |
|---------|----------|
| "pip not found" | Try `pip3 install -r requirements.txt` instead |
| "streamlit not found" | Try `python -m streamlit run Home.py` |
| "Permission denied" | Add `--user` to the pip command: `pip install --user -r requirements.txt` |
| Browser doesn't open | Manually go to `http://localhost:8501` in your browser |

---

## 🤖 Setting Up the Agent Demos (Module 2)

The LLM Cost Explorer (Module 1) and MCP Explorer (Module 3) work without any additional setup.

For the **Multi-Agent Demo** and **LangChain Agent Demo**, the app needs an AI model to run.
You have two options:

### Option A: Ollama — Free, Runs on Your Computer

Ollama lets you run AI models locally. No account, no cost, no data leaving your machine.

| Step | Command |
|------|---------|
| 1. Install Ollama | Download from [ollama.ai](https://ollama.ai) |
| 2. Download a model | `ollama pull llama3.2` (2GB download, one-time) |
| 3. Start Ollama | `ollama serve` — keep this terminal open |

Then run the app (Docker or Python path) and select **Ollama** in the demo settings.

> 💡 The model download is large (~2GB). Do this on a good internet connection.

### Option B: OpenAI — Paid, Faster Results

Costs approximately $0.01 per demo run. Requires creating an account at [platform.openai.com](https://platform.openai.com).

Once you have an API key, enter it directly in the app's sidebar — no environment setup needed.

For full setup instructions for both options, see `docs/CREWAI_SETUP.md`.

---

## 📚 Documentation

| Guide | What It Covers |
|-------|---------------|
| [📥 Student Quick Start (PDF)](docs/Student_Quick_Start.pdf) | Screenshots walkthrough — start here if you're new |
| [🐳 Docker Guide](docs/DOCKER_GUIDE.md) | Full Docker setup with troubleshooting |
| [📖 Beginner's Guide](docs/BEGINNERS_GUIDE.md) | Deep explanation of all technologies used |
| [💰 LLM Cost Guide](docs/LLM_COST_GUIDE.md) | Token economics and model pricing (Module 1) |
| [🤖 Multi-Agent Guide](docs/MULTI_AGENT_GUIDE.md) | CrewAI vs LangChain patterns (Module 2) |
| [🔌 MCP Guide](docs/MCP_GUIDE.md) | Model Context Protocol explained (Module 3) |
| [⚙️ CrewAI Setup](docs/CREWAI_SETUP.md) | Ollama and OpenAI setup for agent demos |

---

## 📁 Project Structure

```
AgenticAI_foundry/
├── Home.py                          # Start here — the course hub
├── pages/
│   ├── 1_LLM_Cost_Calculator.py    # Module 1: Cost explorer
│   ├── 2_Multi_Agent_Demo.py       # Module 2: CrewAI multi-agent
│   ├── 3_LangChain_Agent_Demo.py   # Module 2: LangChain single agent
│   ├── 4_MCP_Explorer.py           # Module 3: MCP protocol
│   ├── 5_Agent_Security_Demo.py    # Module 4: Prompt injection & guardrails
│   └── 6_HITL_Demo.py              # Module 5: Human-in-the-Loop patterns
├── crews/                           # Multi-agent logic (CrewAI)
├── agents/                          # Single-agent logic (LangChain)
├── docs/                            # All guides and documentation
│   ├── Student_Quick_Start.pdf      # ← Start here if you're new
│   ├── DOCKER_GUIDE.md
│   ├── BEGINNERS_GUIDE.md
│   └── ...
├── setup_check.py                   # Run this to check your environment
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔍 Check Your Environment

Not sure if everything is set up correctly? Run this from your terminal in the project folder:

```bash
python setup_check.py
```

It will check Python, required libraries, Docker, Ollama, and API keys — and tell you in plain
English what's working and what needs attention.

---

## 🛠 Technologies Used

| Technology | What It Does |
|-----------|-------------|
| [Streamlit](https://streamlit.io/) | Creates the web interface |
| [CrewAI](https://github.com/joaomdmoura/crewAI) | Orchestrates multiple AI agents |
| [LangChain](https://langchain.com/) | Connects to AI providers and tools |
| [Ollama](https://ollama.ai/) | Runs AI models locally on your machine |
| [Docker](https://www.docker.com/) | Packages the app for reliable deployment |
| [Plotly](https://plotly.com/) | Interactive charts and visualizations |

---

## ❓ Getting Help

- **Setup issues:** Run `python setup_check.py` and share the output
- **Docker problems:** See `docs/DOCKER_GUIDE.md` troubleshooting section
- **Agent demo issues:** See `docs/CREWAI_SETUP.md` troubleshooting section
- **General questions:** Post in the course discussion forum with any error messages you see

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

*MIT Professional Education | Applied Generative AI for Digital Transformation*
*Modules 1, 3, 4 & 5 work immediately with no API key · Module 2 requires Ollama or OpenAI*
