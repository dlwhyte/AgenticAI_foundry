# Understanding the Model Context Protocol (MCP) 🔌

> **MCP Guide** — Part of [AgenticAI Foundry](https://github.com/dlwhyte/AgenticAI_foundry)  
> For MIT Professional Education: Applied Generative AI for Digital Transformation

---

## What is MCP?

The **Model Context Protocol (MCP)** is an open standard that lets AI models talk to external tools and services using a single, universal protocol.

### The USB-C Analogy

Think about what happened with device chargers:

| Before USB-C | With USB-C |
|-------------|------------|
| Mini USB for cameras | One connector for everything |
| Micro USB for phones | Charges your laptop |
| Lightning for iPhones | Transfers files to your phone |
| Barrel plugs for laptops | Connects your monitor |
| DisplayPort for monitors | Works with any brand |

**Before MCP**, every AI model needed a custom integration for every tool it wanted to use. 10 AI models × 10 tools = **100 custom connectors** — fragile, expensive, hard to maintain.

**With MCP**, each AI model implements one standard client, and each tool implements one standard server. 10 AI models + 10 tools = **20 connections**. Build once, connect to anything.

---

## How MCP Works

MCP has three layers:

### 1. AI Model (MCP Client)
The AI model — Claude, GPT, Gemini, etc. — that receives user requests and decides which tools to use.

- Parses natural language into structured intent
- Decides which MCP tools to call and in what order
- Interprets results and responds to the user

### 2. MCP Protocol Layer
The standardized communication format. All messages use **JSON-RPC 2.0** with defined methods:

| Method | What It Does |
|--------|-------------|
| `tools/list` | Discover what tools are available |
| `tools/call` | Invoke a specific tool with parameters |
| `resources/read` | Access data sources |
| `prompts/get` | Retrieve prompt templates |

### 3. MCP Servers (Tools)
External services wrapped in a standard MCP interface. Examples:

- Google Calendar, Outlook
- Slack, Discord, Microsoft Teams
- Salesforce, HubSpot
- GitHub, Jira
- Datadog, PagerDuty
- Spotify, file systems, databases

Each server handles its own authentication, rate limiting, and error handling internally. The AI model doesn't need to know those details.

---

## A Real Example: Scheduling a Meeting

**User says:** "Schedule a meeting with Sarah for next Tuesday at 2pm"

Here's what happens behind the scenes:

| Step | Component | What Happens |
|------|-----------|-------------|
| 1 | **AI Model** | Parses intent: `schedule_meeting(contact='Sarah', date='next Tue', time='2pm')` |
| 2 | **MCP Client** | Discovers available tools → finds `google_calendar` MCP server |
| 3 | **MCP Protocol** | Sends JSON-RPC: `{ method: 'tools/call', params: { name: 'create_event', ... } }` |
| 4 | **Calendar Server** | Checks Sarah's availability, creates event, sends calendar invite |
| 5 | **AI Model** | Returns: "Done — meeting with Sarah scheduled for Tuesday at 2pm" |

The user never sees any JSON or API calls. They speak naturally, and MCP handles the translation.

---

## MCP vs. Other Integration Approaches

| Aspect | Zapier / n8n | Custom APIs | MCP |
|--------|-------------|-------------|-----|
| **Complexity** | Low (no-code) | High (custom dev) | Medium (standard) |
| **AI Awareness** | None — trigger/action | Manual integration | Native AI support |
| **Context / Memory** | No | Build it yourself | Built-in |
| **Multi-step Reasoning** | Limited branching | Possible but complex | Yes — agent-driven |
| **Best For** | Simple automations | Unique business logic | AI agent ecosystems |

### When to Use Each

- **Low technical maturity** (no APIs, no dev team) → **Zapier / n8n**  
  *Example: "Connect Gmail to a Slack notification when a VIP customer emails"*

- **Medium technical maturity** (some APIs, small dev team) → **MCP + existing servers**  
  *Example: "Let our AI assistant query Salesforce and schedule meetings via Google Calendar"*

- **High technical maturity** (full eng team, proprietary systems) → **Custom APIs / MCP servers**  
  *Example: "Build a custom MCP server connecting our AI to our proprietary ERP system"*

---

## Using the MCP Explorer Demo

The MCP Explorer in this repo (`pages/4_MCP_Explorer.py`) lets you:

1. **Walk through scenarios step by step** — See exactly how each layer processes a request, with real JSON-RPC messages
2. **Compare approaches** — Same task shown via Zapier, custom APIs, and MCP
3. **Understand the protocol** — See the three-layer architecture and message format

No API key is needed — it's an educational simulation.

### Running It

```bash
# If running the full app
streamlit run Home.py
# Then click "MCP Explorer" in the sidebar

# Or run it directly
streamlit run pages/4_MCP_Explorer.py
```

---

## Assignment 3 Connection

The MCP Explorer directly supports **Assignment 3, Question 3: How would your agent integrate with existing systems?**

When writing your proposal, consider:

- **Which tools** does your agent need to connect to? (Name them specifically.)
- **Which approach** fits your organization? (Zapier, MCP, custom APIs — and why?)
- **What are the barriers?** (Legacy systems, siloed data, no dev team?)
- **What's your phased rollout?** (MVP with Zapier → scale with MCP?)

A strong answer names specific tools and justifies the integration approach based on your org's technical maturity.

---

## Learn More

- [MCP Specification](https://modelcontextprotocol.io/) — The official MCP documentation
- [MCP Servers Directory](https://github.com/modelcontextprotocol/servers) — Pre-built MCP servers you can use
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol) — Why Anthropic created MCP

---

<p align="center">
  <b>MIT Professional Education | Applied Generative AI for Digital Transformation</b>
</p>
