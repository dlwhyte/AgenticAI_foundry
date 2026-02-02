# Complete Beginner's Guide to Multi-Agent AI 🎓

**MIT Professional Education: Agentic AI Course**

*A step-by-step guide for absolute beginners — no prior AI experience required*

---

## Table of Contents

1. [What You'll Learn](#what-youll-learn)
2. [The Big Picture: What Are AI Agents?](#the-big-picture-what-are-ai-agents)
3. [Understanding the Technology Stack](#understanding-the-technology-stack)
4. [What is Ollama? (Deep Dive)](#what-is-ollama-deep-dive)
5. [What is CrewAI? (Deep Dive)](#what-is-crewai-deep-dive)
6. [How the Demo Works](#how-the-demo-works)
7. [Step-by-Step Setup Guide](#step-by-step-setup-guide)
8. [Running Your First Multi-Agent Task](#running-your-first-multi-agent-task)
9. [Understanding the Output](#understanding-the-output)
10. [Troubleshooting for Beginners](#troubleshooting-for-beginners)
11. [Glossary](#glossary)
12. [Further Reading & Resources](#further-reading--resources)

---

## What You'll Learn

By the end of this guide, you will:

- ✅ Understand what AI agents are and why they matter
- ✅ Know the difference between cloud AI (OpenAI) and local AI (Ollama)
- ✅ Have Ollama running on your computer with a working AI model
- ✅ Run a multi-agent research task and see three AI agents collaborate
- ✅ Understand the code well enough to modify it for your own projects

**Time required:** ~30 minutes for setup, ~10 minutes for your first run

---

## The Big Picture: What Are AI Agents?

### From Chatbots to Agents

You're probably familiar with AI chatbots like ChatGPT or Claude. You type a question, and they respond. This is called a **single-turn interaction** — you ask, they answer.

**AI Agents** are different. They can:

1. **Break down complex tasks** into smaller steps
2. **Take actions** (search the web, write files, call APIs)
3. **Work together** with other agents
4. **Operate with minimal human intervention**

Think of the difference like this:

| Chatbot | Agent |
|---------|-------|
| Answers questions | Completes tasks |
| Single response | Multiple steps |
| You guide every step | Works autonomously |
| Like a reference librarian | Like a research assistant |

### Why Multi-Agent Systems?

Imagine you need a research report. With a single AI, you'd prompt it to do everything — research, write, and edit. The results are often mediocre because no single prompt can capture all those requirements.

**Multi-agent systems** solve this by having **specialized agents**:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ RESEARCHER  │ →  │   WRITER    │ →  │   EDITOR    │
│             │    │             │    │             │
│ Gathers     │    │ Transforms  │    │ Polishes    │
│ facts &     │    │ research    │    │ for clarity │
│ data        │    │ into prose  │    │ & accuracy  │
└─────────────┘    └─────────────┘    └─────────────┘
```

Each agent has:
- A **role** (what they do)
- A **goal** (what they're trying to achieve)
- A **backstory** (context that shapes their behavior)

This is exactly what our demo does!

---

## Understanding the Technology Stack

Before we dive into setup, let's understand what each piece of technology does:

```
┌────────────────────────────────────────────────────────┐
│                    YOUR BROWSER                         │
│                  (localhost:8501)                       │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│                     STREAMLIT                           │
│         (Web interface - makes it pretty)               │
│                                                         │
│  File: pages/2_Multi_Agent_Demo.py                     │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│                      CREWAI                             │
│    (Orchestrates agents - makes them work together)     │
│                                                         │
│  File: crews/research_crew.py                          │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│              LANGUAGE MODEL (LLM)                       │
│         (The actual AI brain doing the thinking)        │
│                                                         │
│  Option A: Ollama (local, free)                        │
│  Option B: OpenAI (cloud, paid)                        │
└────────────────────────────────────────────────────────┘
```

### Technology Summary

| Technology | What It Does | Analogy |
|------------|--------------|---------|
| **Streamlit** | Creates the web interface | The "front desk" |
| **CrewAI** | Coordinates multiple agents | The "project manager" |
| **LangChain** | Connects to different AI providers | The "translator" |
| **Ollama** | Runs AI models locally | Your "in-house AI team" |
| **OpenAI API** | Cloud AI service | "Outsourced AI consultants" |

---

## What is Ollama? (Deep Dive)

### The Problem Ollama Solves

Traditionally, to use powerful AI models, you needed to:
1. Send your data to a company's servers (privacy concern)
2. Pay per request (cost adds up)
3. Have internet access (dependency)
4. Wait for network round-trips (latency)

**Ollama** lets you run the same AI models **entirely on your own computer**.

### How Ollama Works

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                         │
│                                                          │
│  ┌─────────────┐     ┌─────────────────────────────┐   │
│  │   Ollama    │     │     Downloaded Models        │   │
│  │   Server    │ ←── │                              │   │
│  │             │     │  • llama3.2 (4.7 GB)        │   │
│  │ localhost   │     │  • mistral (4.1 GB)         │   │
│  │ :11434      │     │  • phi3 (2.3 GB)            │   │
│  └─────────────┘     └─────────────────────────────┘   │
│         ↑                                               │
│         │                                               │
│  ┌──────┴──────┐                                       │
│  │ Your Apps   │  (Our demo connects here)             │
│  └─────────────┘                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Key Ollama Concepts

**1. Models**
A "model" is the trained AI brain. Different models have different capabilities:

| Model | Size | Best For | Speed |
|-------|------|----------|-------|
| `phi3` | 2.3 GB | Quick tasks, limited RAM | ⚡⚡⚡ Fast |
| `mistral` | 4.1 GB | Good balance | ⚡⚡ Medium |
| `llama3.2` | 4.7 GB | General use (recommended) | ⚡⚡ Medium |
| `llama3.1` | 8.5 GB | Complex reasoning | ⚡ Slower |

**2. Server**
Ollama runs as a "server" on your computer. It listens on port 11434 for requests. When your app asks for AI help, Ollama:
1. Receives the request
2. Loads the model (if not already loaded)
3. Processes your input
4. Returns the response

**3. Commands**
```bash
ollama serve    # Start the server (required first!)
ollama pull     # Download a model
ollama list     # See your downloaded models
ollama run      # Chat with a model directly
```

### Ollama vs. OpenAI Comparison

| Aspect | Ollama | OpenAI |
|--------|--------|--------|
| **Cost** | Free | ~$0.01 per demo run |
| **Privacy** | Data stays on your machine | Data sent to OpenAI |
| **Speed** | Depends on your hardware | Consistently fast |
| **Setup** | More complex | Just need API key |
| **Internet** | Not required | Required |
| **Quality** | Good (varies by model) | Excellent |

**When to use Ollama:**
- Learning/experimenting (no cost)
- Privacy-sensitive data
- Offline work
- Understanding how AI works "under the hood"

**When to use OpenAI:**
- Production applications
- Fastest results needed
- Don't want to manage local setup

---

## What is CrewAI? (Deep Dive)

### The Problem CrewAI Solves

Single AI models, even powerful ones, struggle with complex tasks because:
- They have no memory between responses
- They can't break tasks into steps autonomously
- They don't have specialized skills for different subtasks

**CrewAI** is a framework that lets you create **teams of AI agents** that:
- Have specific roles and expertise
- Pass work to each other
- Remember context within a session
- Work toward a shared goal

### How CrewAI Specializes Agents

CrewAI agents are **not** raw API calls or simple prompt templates. Instead, CrewAI uses an abstraction layer where you define agents with **three key attributes**:

| Attribute | Purpose | Example |
|-----------|---------|---------|
| **Role** | The agent's job title | "Research Analyst" |
| **Goal** | What the agent is trying to achieve | "Gather comprehensive information about {topic}" |
| **Backstory** | Context that shapes behavior and expertise | "You are an experienced researcher with expertise in finding accurate, relevant information..." |

**What happens under the hood:**

1. You define `role`, `goal`, and `backstory` for each agent
2. CrewAI combines these with the task description
3. CrewAI constructs a system prompt + user prompt internally
4. The prompt is sent to the LLM (OpenAI, Ollama, etc.) via API call

This abstraction lets you define agent "personalities" without writing raw prompts. Think of it like hiring team members — you describe *who they are*, and CrewAI handles *how to instruct them*.

### How CrewAI Works

```python
# This is simplified - see the actual code in crews/research_crew.py

from crewai import Agent, Task, Crew

# 1. Define specialized agents
researcher = Agent(
    role="Research Analyst",
    goal="Gather comprehensive information",
    backstory="You are an experienced researcher..."
)

writer = Agent(
    role="Content Writer", 
    goal="Transform research into clear content",
    backstory="You excel at making complex topics accessible..."
)

editor = Agent(
    role="Editor",
    goal="Polish content for publication",
    backstory="You have an eye for detail..."
)

# 2. Define tasks with dependencies
research_task = Task(
    description="Research the topic thoroughly",
    agent=researcher
)

writing_task = Task(
    description="Write a clear brief from the research",
    agent=writer,
    context=[research_task]  # Gets output from research
)

editing_task = Task(
    description="Polish the written content",
    agent=editor,
    context=[writing_task]  # Gets output from writer
)

# 3. Create the crew and run
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task]
)

result = crew.kickoff()
```

### The Agent Workflow

```
USER INPUT: "Research AI in healthcare"
              │
              ▼
    ┌─────────────────┐
    │   RESEARCHER    │
    │                 │
    │ Receives topic  │
    │ Gathers info    │
    │ Outputs brief   │
    └────────┬────────┘
             │ passes research to...
             ▼
    ┌─────────────────┐
    │     WRITER      │
    │                 │
    │ Receives brief  │
    │ Writes content  │
    │ Outputs draft   │
    └────────┬────────┘
             │ passes draft to...
             ▼
    ┌─────────────────┐
    │     EDITOR      │
    │                 │
    │ Receives draft  │
    │ Polishes text   │
    │ Outputs final   │
    └────────┬────────┘
             │
             ▼
      FINAL OUTPUT
```

---

## How the Demo Works

Our demo combines all these technologies:

### File Structure Explained

```
AgenticAI_foundry/
│
├── Home.py                         # Landing page (what you see first)
│
├── pages/
│   ├── 1_LLM_Cost_Calculator.py   # Module 1 demo
│   └── 2_Multi_Agent_Demo.py      # Module 2 demo ← The agent demo
│
├── crews/                          # 🚀 THE HEART OF MULTI-AGENT LOGIC
│   ├── __init__.py                # Makes this a Python package
│   └── research_crew.py           # The actual agent definitions & orchestration
│
└── docs/
    ├── DOCKER_GUIDE.md            # Docker setup help
    ├── CREWAI_SETUP.md            # Quick setup reference
    └── BEGINNERS_GUIDE.md         # This file!
```

### What is the `crews/` Folder?

The `crews/` folder is where all the **multi-agent logic** lives. Think of it as the "brain" of the demo while the `pages/` folder is the "face" (the user interface).

**Why separate them?**

| Folder | Purpose | Analogy |
|--------|---------|---------|
| `pages/` | User interface (buttons, displays) | The dashboard of a car |
| `crews/` | Agent logic (AI coordination) | The engine under the hood |

This separation means you can:
- **Reuse crews** in different interfaces (web, CLI, API)
- **Test agents** independently of the UI
- **Build new crews** for different tasks (sales, support, analysis)

### Inside `research_crew.py`

This file contains everything needed to run a multi-agent research team:

```python
# 1. CONFIGURATION - Define providers (Ollama, OpenAI)
PROVIDER_CONFIGS = {
    "ollama": ProviderConfig(...),    # Free, local AI
    "openai": ProviderConfig(...),    # Paid, cloud AI
}

# 2. TELEMETRY - Track performance metrics
@dataclass
class AgentTelemetry:
    duration_seconds: float    # How long agent took
    input_tokens: int          # Tokens sent to AI
    output_tokens: int         # Tokens received back
    ...

# 3. AGENT DEFINITIONS - The three specialists
def create_research_crew(llm):
    researcher = Agent(
        role="Research Analyst",
        goal="Gather comprehensive, accurate information",
        backstory="You are an experienced researcher..."
    )
    writer = Agent(...)
    editor = Agent(...)
    return {"Researcher": researcher, "Writer": writer, "Editor": editor}

# 4. TASK DEFINITIONS - What each agent does
def create_tasks(agents, topic):
    research_task = Task(description=f"Research {topic}...", agent=agents["Researcher"])
    writing_task = Task(description="Write a brief...", agent=agents["Writer"])
    editing_task = Task(description="Polish the content...", agent=agents["Editor"])
    return [research_task, writing_task, editing_task]

# 5. EXECUTION - Run the crew and collect telemetry
def run_research_crew(topic, provider, ...):
    llm = get_llm(provider)           # Get AI model
    agents = create_research_crew(llm) # Create agents
    tasks = create_tasks(agents, topic) # Define tasks
    crew = Crew(agents=..., tasks=...)  # Assemble crew
    result = crew.kickoff()             # Run!
    return CrewResult(output=result, telemetry=...)
```

### How the UI and Crews Connect

When you click "Run Research Crew" in the browser:

```
┌─────────────────────────────────────────────────────────────────┐
│  BROWSER (what you see)                                         │
│  pages/2_Multi_Agent_Demo.py                                    │
│                                                                 │
│  ┌─────────────────┐                                           │
│  │ [Run Research]  │ ◄── You click this                        │
│  └────────┬────────┘                                           │
└───────────┼─────────────────────────────────────────────────────┘
            │
            │ calls
            ▼
┌─────────────────────────────────────────────────────────────────┐
│  CREWS ENGINE (what runs behind the scenes)                     │
│  crews/research_crew.py                                         │
│                                                                 │
│  run_research_crew(topic="AI in healthcare", provider="ollama") │
│            │                                                    │
│            ├── Creates LLM connection                          │
│            ├── Creates 3 agents                                │
│            ├── Creates 3 tasks                                 │
│            ├── Runs Crew.kickoff()                             │
│            └── Returns result + telemetry                      │
└─────────────────────────────────────────────────────────────────┘
            │
            │ returns
            ▼
┌─────────────────────────────────────────────────────────────────┐
│  BROWSER (displays results)                                     │
│                                                                 │
│  📊 Summary Metrics: 45.2s | 3,421 tokens | $0.0012            │
│  📄 Final Output: "AI in healthcare is transforming..."        │
│  📈 Charts: Duration by agent, Token usage                     │
└─────────────────────────────────────────────────────────────────┘
```

### Building Your Own Crews

Once you understand this pattern, you can create new crews for any task:

```python
# Example: Customer Support Crew
support_crew/
├── __init__.py
└── support_crew.py
    ├── intake_agent      # Understands customer issue
    ├── solution_agent    # Finds answers in knowledge base
    └── response_agent    # Crafts friendly reply

# Example: Code Review Crew  
code_crew/
├── __init__.py
└── code_crew.py
    ├── analyzer_agent    # Reads and understands code
    ├── security_agent    # Checks for vulnerabilities
    └── reviewer_agent    # Suggests improvements
```

The pattern is always the same:
1. **Define agents** with roles, goals, backstories
2. **Define tasks** with descriptions and agent assignments
3. **Create a crew** and call `kickoff()`

### What Happens When You Click "Run"

```
1. You enter a topic in Streamlit
           │
           ▼
2. Streamlit calls crews/research_crew.py
           │
           ▼
3. research_crew.py creates 3 agents
           │
           ▼
4. CrewAI orchestrates the workflow
           │
           ▼
5. Each agent calls Ollama (or OpenAI) to "think"
           │
           ▼
6. Results flow back through Streamlit
           │
           ▼
7. You see the final output!
```

---

## Step-by-Step Setup Guide

### Prerequisites Check

Before starting, verify you have:

- [ ] **Python 3.9 or newer** — Check with `python --version`
- [ ] **pip** — Check with `pip --version`  
- [ ] **8+ GB RAM** — Required for local AI models
- [ ] **10+ GB free disk space** — Models are large files

### Step 1: Install Ollama

**macOS:**
```bash
# Using Homebrew (recommended)
brew install ollama

# Or download from https://ollama.ai
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
1. Go to [ollama.ai](https://ollama.ai)
2. Click "Download"
3. Run the installer
4. Open a new terminal after installation

**Verify installation:**
```bash
ollama --version
# Should show something like: ollama version 0.1.x
```

### Step 2: Download an AI Model

```bash
# Download the recommended model (takes 2-5 minutes)
ollama pull llama3.2

# Verify it downloaded
ollama list
# Should show: llama3.2:latest
```

**What's happening:** Ollama is downloading a 4.7 GB file containing the trained neural network. This only happens once — the model is saved locally.

### Step 3: Start the Ollama Server

```bash
ollama serve
```

**Leave this terminal open!** You should see:
```
Couldn't find '/Users/you/.ollama/id_ed25519'. Generating new private key.
Your new public key is: ...
2024/01/15 10:30:00 routes.go:1019: INFO server config...
```

**What's happening:** Ollama is now listening on `http://localhost:11434` for AI requests.

### Step 4: Clone the Repository

Open a **new terminal** (keep Ollama running in the other):

```bash
# Navigate to where you want the project
cd ~/Projects  # or wherever you prefer

# Clone the repo
git clone https://github.com/dlwhyte/AgenticAI_foundry.git

# Enter the directory
cd AgenticAI_foundry
```

### Step 5: Set Up Python Environment

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Your prompt should now show (venv)
```

### Step 6: Install Dependencies

```bash
# Install base requirements
pip install -r requirements.txt

# Install CrewAI and Ollama support
pip install crewai langchain-community
```

### Step 7: Verify Everything Works

```bash
# Check that Ollama is accessible
curl http://localhost:11434/api/tags

# Should return JSON with your models

# Or use our built-in check
python -m crews.research_crew --check
```

You should see:
```
🔍 Checking provider availability...

  ✅ 🏠 Ollama (Local)
      └─ Ollama is running
      └─ llama3.2 model available
  ✅ ☁️ OpenAI
      └─ ⚠️  No API key. Set OPENAI_API_KEY
```

### Step 8: Launch the App

```bash
streamlit run Home.py
```

Your browser should open to `http://localhost:8501`. Click **"Multi-Agent Demo"** in the sidebar!

---

## Running Your First Multi-Agent Task

### Using the Streamlit Interface

1. **Select Provider:** Choose "🏠 Ollama (Local)" in the sidebar
2. **Enter a Topic:** Try something like:
   - "Research the impact of AI on healthcare"
   - "Explain quantum computing for business leaders"
   - "Summarize recent developments in renewable energy"
3. **Click "🚀 Run Research Crew"**
4. **Watch the agents work!**

### Using the Command Line

For more control, use the CLI directly:

```bash
# Basic usage
python -m crews.research_crew --provider ollama --task "Research AI in education"

# See what's happening (verbose mode is on by default)
python -m crews.research_crew --provider ollama --task "Explain blockchain"

# Quiet mode (just the result)
python -m crews.research_crew --provider ollama --task "Topic" --quiet
```

---

## Understanding the Output

When the demo runs, you'll see output like this:

```
====================================================================
🤖 CrewAI Research Team
====================================================================
Provider: 🏠 Ollama (Local)
Model:    llama3.2
Topic:    Research AI in healthcare
====================================================================

📌 Initializing 🏠 Ollama (Local)...
📌 Creating agents...
📌 Setting up tasks...
📌 🔍 Researcher is gathering information...

[Agent: Research Analyst] Starting research on AI in healthcare...
[Agent: Research Analyst] Key findings:
  - AI diagnostic accuracy rates...
  - Implementation challenges...
  
[Agent: Content Writer] Transforming research into prose...

[Agent: Editor] Polishing final output...

====================================================================
✅ FINAL OUTPUT
====================================================================

[The polished research brief appears here]
```

### What Each Agent Does

**Researcher Output:**
- Raw facts and statistics
- Key trends and developments
- Notable examples
- Unstructured but comprehensive

**Writer Output:**
- Organized prose
- Clear introduction, body, conclusion
- Accessible language
- 300-500 words

**Editor Output:**
- Polished final version
- Corrected any errors
- Improved clarity
- Publication-ready

---

## Troubleshooting for Beginners

### "Ollama not running"

**Symptom:** Error says Ollama isn't available

**Fix:**
```bash
# In a separate terminal:
ollama serve

# Keep it running while using the demo
```

### "Model not found"

**Symptom:** Error about missing model

**Fix:**
```bash
# Download the model
ollama pull llama3.2

# Verify it's there
ollama list
```

### "Out of memory"

**Symptom:** Computer freezes or error about memory

**Fix:**
1. Close other applications
2. Try a smaller model:
```bash
ollama pull phi3
# Then select phi3 in the demo or use --model phi3
```

### "Very slow responses"

**Symptom:** Taking many minutes per agent

**This is normal for local models!** Tips:
- First run is slowest (loading model)
- Smaller models are faster (`phi3` vs `llama3.1`)
- GPU acceleration helps dramatically
- Consider OpenAI for speed-critical work

### "Import errors"

**Symptom:** Python can't find modules

**Fix:**
```bash
# Make sure you're in the right directory
cd AgenticAI_foundry

# Make sure venv is activated
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
pip install crewai langchain-community
```

### "Permission denied"

**Symptom:** Can't run scripts or access files

**Fix (macOS/Linux):**
```bash
chmod +x ollama  # If needed for Ollama
```

**Fix (Windows):**
- Run terminal as Administrator
- Check antivirus isn't blocking

---

## Glossary

| Term | Definition |
|------|------------|
| **Agent** | An AI entity with a specific role, goal, and capabilities |
| **API** | Application Programming Interface — how programs talk to each other |
| **API Key** | A secret password that lets you use a service (like OpenAI) |
| **CLI** | Command Line Interface — using text commands instead of clicking |
| **Context Window** | How much text an AI can "remember" at once |
| **CrewAI** | A Python framework for building multi-agent systems |
| **Hallucination** | When AI makes up false information confidently |
| **LangChain** | A library that connects to different AI providers |
| **LLM** | Large Language Model — the AI brain (like GPT, Llama, etc.) |
| **Local Model** | AI running on your own computer, not in the cloud |
| **Model** | The trained AI "brain" — a large file of learned patterns |
| **Ollama** | Software that runs AI models locally on your computer |
| **OpenAI** | Company that makes GPT models, accessed via their cloud API |
| **Prompt** | The input/instructions you give to an AI |
| **Server** | A program that waits for and responds to requests |
| **Streamlit** | A Python library for creating web apps quickly |
| **Token** | A chunk of text (~4 characters) — how AI "sees" words |
| **venv** | Virtual environment — isolated Python setup for a project |

---

## Further Reading & Resources

### Official Documentation

- **CrewAI:** [docs.crewai.com](https://docs.crewai.com)
- **Ollama:** [github.com/ollama/ollama](https://github.com/ollama/ollama)
- **Streamlit:** [docs.streamlit.io](https://docs.streamlit.io)
- **LangChain:** [python.langchain.com](https://python.langchain.com)

### Tutorials & Courses

- **DeepLearning.AI:** Free courses on AI agents
- **YouTube:** Search "CrewAI tutorial" for video walkthroughs
- **Ollama Blog:** [ollama.ai/blog](https://ollama.ai/blog) for tips and updates

### Community

- **CrewAI Discord:** Active community for questions
- **r/LocalLLaMA:** Reddit community for local AI
- **Ollama Discord:** Help with local model setup

### Books

- *"Building LLM Apps"* by Valentino Gagliardi
- *"Generative AI with LangChain"* by Ben Auffarth

### Next Steps After This Demo

1. **Modify the agents:** Edit `crews/research_crew.py` to change their personalities
2. **Add new agents:** Create a "Fact Checker" or "Translator" agent
3. **Connect tools:** CrewAI supports web search, file reading, and more
4. **Build your own crew:** Design agents for your specific use case

---

## Summary

You've learned:

1. **AI Agents** are autonomous entities that can complete multi-step tasks
2. **Ollama** runs AI models locally on your computer (free, private)
3. **CrewAI** orchestrates multiple agents working together
4. **Our demo** shows Researcher → Writer → Editor collaboration
5. **Setup** involves: Ollama + model + Python environment + our code

**The key insight:** Multi-agent systems can achieve better results than single models by having specialists collaborate — just like human teams.

---

<p align="center">
  <b>MIT Professional Education | Agentic AI Course</b><br>
  <i>Module 2: Multi-Agent Systems</i><br><br>
  Questions? Check the <a href="CREWAI_SETUP.md">Quick Setup Guide</a> or ask in class!
</p>

---

## How CrewAI Specializes Agents

> 📊 **See Also**: Slides "How CrewAI Specializes Agents" and "What Happens Under the Hood" in the presentation deck.

A common question: Are CrewAI agents custom prompt templates or raw API calls?

**Answer**: Neither — it's an abstraction layer that handles both.

### The Three Key Attributes

When you define an agent in CrewAI, you specify three things:

| Attribute | Purpose | Example |
|-----------|---------|---------|
| **Role** | The agent's job title | "Research Analyst" |
| **Goal** | What the agent is trying to achieve | "Gather comprehensive information about {topic}" |
| **Backstory** | Context that shapes behavior and expertise | "You are an experienced researcher with expertise in finding accurate, relevant information..." |

### Code Example (from `research_crew.py`)

```python
Agent(
    role="Research Analyst",
    goal="Gather comprehensive information about {topic}",
    backstory="You are an experienced researcher with expertise in finding accurate, relevant information...",
    llm=llm,
    verbose=verbose
)
```

### What Happens Under the Hood

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌──────────┐
│ Your Definition │ >>> │     CrewAI      │ >>> │    LLM API      │ >>> │  Output  │
│ role, goal,     │     │ Builds prompt   │     │ OpenAI / Ollama │     │  Agent   │
│ backstory       │     │ from attributes │     │                 │     │  result  │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └──────────┘
```

1. **You define** the agent with role, goal, and backstory
2. **CrewAI combines** these with the task description to construct a system prompt
3. **The prompt is sent** to the LLM via API (OpenAI, Ollama, etc.)
4. **The response** becomes the agent's output

### Key Insight

CrewAI is an **abstraction layer** — you define "personalities" without writing raw prompts. This lets you:

- Focus on **what** agents should do, not **how** to prompt them
- Easily swap LLM providers (OpenAI ↔ Ollama) without changing agent definitions
- Create reusable agent "templates" for different use cases

### Why This Matters for the Demo

In the Multi-Agent Demo, you'll see three agents (Researcher, Writer, Editor) with different roles, goals, and backstories. Each produces distinct output because CrewAI constructs different prompts based on their attributes — even though they're all using the same underlying LLM.

---

## The `agents/` Folder — LangChain Single-Agent Logic

While `crews/` contains CrewAI multi-agent logic, the `agents/` folder contains **LangChain single-agent** implementations.

### What's the Difference?

| Folder | Framework | Pattern | Example |
|--------|-----------|---------|---------|
| `crews/` | CrewAI | Multi-agent collaboration | Researcher → Writer → Editor |
| `agents/` | LangChain | Single agent + tools | Agent + Web Search |

### Inside `agents/crypto_agent.py`

This file implements a LangChain agent that:
1. Takes a question about cryptocurrency prices
2. Uses the **DuckDuckGo search tool** to get real-time data
3. Returns a formatted answer

**Key Components:**

```python
# The LLM (brain)
llm = ChatOpenAI(model="gpt-4o-mini")  # or ChatOllama

# The tool (capability)
search_tool = DuckDuckGoSearchRun()

# The agent (combines brain + tools)
agent = create_react_agent(llm, [search_tool], prompt)

# Run it
result = agent_executor.invoke({"input": "What's the Bitcoin price?"})
```

### The ReAct Pattern

LangChain agents use the **ReAct** (Reasoning + Acting) pattern:

```
Question: What's the current price of Bitcoin?
    │
    ▼
Thought: I need to search for current Bitcoin price
    │
    ▼
Action: web_search("Bitcoin current price")
    │
    ▼
Observation: Bitcoin is trading at $97,245...
    │
    ▼
Thought: I now have the information
    │
    ▼
Final Answer: Bitcoin is currently trading at $97,245.
```

### When to Use Which?

| Scenario | Use This |
|----------|----------|
| Multi-step workflow with handoffs | **CrewAI** (crews/) |
| Need real-time data from tools | **LangChain** (agents/) |
| Research → Write → Edit pipeline | **CrewAI** |
| Quick question with search | **LangChain** |
