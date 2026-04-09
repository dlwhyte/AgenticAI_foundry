# 🧑‍✈️ Module 5: Human-in-the-Loop (HITL) — Guide

## What Is Human-in-the-Loop?

A fully autonomous AI agent is powerful — but in high-stakes or irreversible situations, you need a human to review and approve before the agent acts. This is called **Human-in-the-Loop (HITL)**.

HITL is not a weakness in your AI system. It is an **architectural pattern** used by every serious enterprise AI deployment. The goal is not to make agents less capable — it is to make them **trustworthy enough to deploy at scale**.

---

## The Three HITL Patterns in This Demo

### Pattern 1: Approval Gate (Binary Review)

The simplest HITL pattern. The agent proposes an action, assigns a risk score, and then:

- **Low risk** → agent proceeds automatically
- **High risk** → human must explicitly approve or reject

**When to use it:**
- Financial transactions above a threshold
- Sending external communications (emails, API calls)
- Deleting or modifying records

**How it looks in the demo:**
> The agent proposes an action (e.g., "Transfer $4,200 to vendor account"). The risk scorer evaluates it. If risk > threshold, a green/red approval panel appears. The human clicks Approve or Reject. The agent only proceeds after approval.

---

### Pattern 2: Confidence Threshold (Uncertain AI)

Instead of all-or-nothing approval, the agent expresses its own **uncertainty**. When confidence drops below a threshold, the agent pauses and asks for clarification or a human decision.

**When to use it:**
- Medical or legal advice where wrong answers have consequences
- Classification tasks where training data may not cover the input
- Any domain where "I don't know" is safer than a hallucinated answer

**How it looks in the demo:**
> The agent processes a query and reports its confidence (0-100%). High confidence → answer delivered. Low confidence → the agent surfaces the uncertainty and asks the human to confirm or redirect.

---

### Pattern 3: Audit Trail (Review After the Fact)

Not all HITL is real-time. Sometimes agents run autonomously but every action is logged, and humans **review the audit log** periodically to catch errors, drift, or misuse.

**When to use it:**
- High-throughput systems where real-time review is impractical
- Compliance and regulatory requirements (GDPR, HIPAA, SOC 2)
- Detecting prompt injection or adversarial inputs after the fact
- Training data collection — human reviewers grade agent outputs

**How it looks in the demo:**
> The agent runs a series of automated actions. Each is logged with timestamp, action type, risk score, and outcome. The human reviews the log and can flag items for further investigation.

---

## Why HITL Matters for Agentic AI

| Without HITL | With HITL |
|---|---|
| Agent mistakes propagate silently | Errors caught before irreversible action |
| No accountability trail | Full audit log for compliance |
| Hard to debug failures | Clear human decision points |
| Users don't trust the system | Trust built through transparency |
| Regulatory exposure | Defensible AI governance |

### The HITL Spectrum

```
Full Autonomy <---------------------------------------------> Full Manual
     |                                                              |
     |   Low stakes,        Mixed,           High stakes,          |
     |   reversible         moderate         irreversible           |
     |   actions            risk             actions                |
     |                                                              |
     +-- Agent acts -- Agent proposes -- Human decides ------------+
                        Human approves
```

Pick the right point on this spectrum for each action type in your system. Most production agentic systems use **different thresholds for different action categories**.

---

## Running the Demo

### No API Key Required
This demo is fully simulated — no OpenAI key needed.

### Docker (Recommended)
```bash
docker build -t agenticai-foundry .
docker run -p 8501:8501 agenticai-foundry
```
Open http://localhost:8501 and click **Human-in-the-Loop** in the sidebar.

### Python
```bash
pip install -r requirements.txt
python -m streamlit run Home.py
```

### Controls
| Control | What It Does |
|---|---|
| Risk threshold slider | Set the score above which actions require human approval |
| Auto-approve low-risk checkbox | Let the agent self-approve actions below threshold |
| Pattern tabs | Switch between Approval Gate, Confidence Threshold, and Audit Trail |
| Run Agent button | Trigger a simulated agent action |

---

## HITL in Real Systems

### CrewAI (Module 2)
CrewAI supports HITL via `human_input=True` on any task:
```python
task = Task(
    description="Draft a contract amendment for client review",
    agent=legal_agent,
    human_input=True  # pauses and prompts for human review
)
```

### LangChain (Module 2b)
LangChain supports HITL via `HumanApprovalCallbackHandler`:
```python
from langchain.callbacks import HumanApprovalCallbackHandler
tool = Tool(
    name="send_email",
    func=send_email_function,
    callbacks=[HumanApprovalCallbackHandler()]
)
```

### Custom Systems
At minimum, implement:
1. **Action classification** — categorise every action by risk level
2. **Approval queue** — store pending actions in a database
3. **Review interface** — a simple UI for human reviewers
4. **Audit log** — append-only log of all actions and decisions

---

## Key Takeaways

1. **HITL is a spectrum** — not binary. Design different thresholds for different action types.
2. **Risk scoring is the foundation** — you need a consistent way to assess action risk before you can route to humans.
3. **Audit logs are always worth it** — even for fully autonomous actions, log everything.
4. **Trust is built incrementally** — start with high HITL, reduce as the system proves reliable.
5. **Regulations are driving adoption** — EU AI Act, NIST AI RMF, and sector-specific rules increasingly require human oversight for high-risk AI.

---

## Related Modules

- **Module 4 — Agent Security**: Covers prompt injection attacks that try to bypass HITL controls
- **Module 2 — Multi-Agent**: Shows how HITL integrates with multi-agent orchestration in CrewAI
- **GenAI Foundry Notebook 12** — [What is an Agent?](https://github.com/dlwhyte/GenAI_foundry/blob/main/notebooks/what_is_an_agent.ipynb) — prerequisite reading on the Observe→Think→Act loop

---

*MIT Professional Education | Applied Generative AI for Digital Transformation*
