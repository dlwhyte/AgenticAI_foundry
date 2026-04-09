import streamlit as st
import time

st.set_page_config(page_title="Human-in-the-Loop", page_icon="🧑\u200d✈️", layout="wide")

st.title("🧑\u200d✈️ Human-in-the-Loop (HITL) Agent")
st.markdown("""
### Module 5: When Should an Agent Pause and Ask?

A fully autonomous agent is powerful — but in high-stakes situations, you want
a human to review before the agent acts. This is called **Human-in-the-Loop (HITL)**.

This demo shows three HITL patterns used in real enterprise AI systems.
No API key required — all simulated.
""")

# ── Sidebar ──────────────────────────────────────────────
st.sidebar.header("⚙️ Settings")
risk_threshold = st.sidebar.slider(
    "Risk threshold for human review",
    min_value=0, max_value=100, value=60,
    help="Actions scored above this threshold require human approval"
)
auto_approve_low = st.sidebar.checkbox("Auto-approve low-risk actions", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**📚 Related Modules**
- [Module 4: Agent Security](./5_Agent_Security_Demo)
- [GenAI Foundry](https://github.com/dlwhyte/GenAI_foundry)
""")

# ── Simulated task queue ──────────────────────────────────
AGENT_TASKS = [
    {"id": 1, "description": "Search the web for competitor pricing",         "risk_score": 10, "action": "web_search",     "reversible": True},
    {"id": 2, "description": "Draft email to 500 customers about a recall",   "risk_score": 85, "action": "send_email",     "reversible": False},
    {"id": 3, "description": "Delete temporary log files older than 30 days", "risk_score": 55, "action": "delete_files",   "reversible": False},
    {"id": 4, "description": "Update product price in database: $49 → $79",   "risk_score": 72, "action": "db_write",       "reversible": True},
    {"id": 5, "description": "Generate weekly summary report",                "risk_score": 15, "action": "generate_report","reversible": True},
]

# ═══════════════════════════════════════════════════════════
st.divider()
st.subheader("🎬 Pattern 1: Risk-Based Approval Gates")
st.markdown("""
The agent scores each action by risk level. High-risk actions **pause** and wait for
human approval. Low-risk actions run automatically — keeping the agent fast where it's safe.
""")

col_h1, col_h2, col_h3 = st.columns([3, 1, 2])
col_h1.markdown("**Task**")
col_h2.markdown("**Risk**")
col_h3.markdown("**Status**")
st.markdown("---")

if st.button("▶️ Run Agent Task Queue", key="run_queue"):
    for task in AGENT_TASKS:
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            st.write(f"📋 {task['description']}")
        with col2:
            if task["risk_score"] >= risk_threshold:
                st.markdown(f"🔴 **{task['risk_score']}**")
            elif task["risk_score"] >= 40:
                st.markdown(f"🟡 **{task['risk_score']}**")
            else:
                st.markdown(f"🟢 **{task['risk_score']}**")
        with col3:
            if task["risk_score"] >= risk_threshold:
                st.warning("⏸️ PAUSED — needs human approval")
            elif auto_approve_low:
                st.success("✅ Auto-approved & executed")
            else:
                st.info("⏳ Queued for review")
        time.sleep(0.2)

    st.info(f"ℹ️ Threshold set to {risk_threshold}. Adjust in the sidebar to see different outcomes.")

# ═══════════════════════════════════════════════════════════
st.divider()
st.subheader("🎬 Pattern 2: Approval Workflow")
st.markdown("""
The agent **proposes** an action and waits. A human reviews, optionally edits,
then approves or rejects. Only then does the agent proceed.
This pattern is ideal for irreversible or public-facing actions.
""")

scenario = st.selectbox("Choose a scenario:", [
    "Agent wants to send a customer refund email",
    "Agent wants to post to the company social media",
    "Agent wants to cancel a vendor contract",
], key="scenario_select")

PROPOSALS = {
    "Agent wants to send a customer refund email": {
        "fields": {"To": "affected_customers@list.com (247 recipients)",
                   "Subject": "Your refund has been processed",
                   "Body": "Dear Customer, we have processed a full refund of $49.99..."},
        "risk_label": "⚠️ Mass email — cannot be unsent",
        "risk_level": "warning"
    },
    "Agent wants to post to the company social media": {
        "fields": {"Platform": "LinkedIn + Twitter/X",
                   "Content": "Exciting news! We're launching our new AI product next Tuesday. #AI #Innovation",
                   "Scheduled": "Immediately"},
        "risk_label": "⚠️ Public-facing — visible to all followers",
        "risk_level": "warning"
    },
    "Agent wants to cancel a vendor contract": {
        "fields": {"Vendor": "CloudStorage Inc.",
                   "Notice Period": "30 days",
                   "Estimated Annual Savings": "$2,400"},
        "risk_label": "🔴 Irreversible — triggers legal notice period immediately",
        "risk_level": "error"
    }
}

proposal = PROPOSALS[scenario]
st.markdown("**🤖 Agent's proposed action:**")
for key, val in proposal["fields"].items():
    st.write(f"- **{key}:** {val}")

if proposal["risk_level"] == "error":
    st.error(proposal["risk_label"])
else:
    st.warning(proposal["risk_label"])

col_a, col_b = st.columns(2)
with col_a:
    if st.button("✅ Approve — Agent proceeds", key="approve_btn"):
        st.success("✅ Action approved! Agent is now executing the task...")
        st.balloons()
with col_b:
    if st.button("❌ Reject — Agent stops", key="reject_btn"):
        st.error("❌ Action rejected. Agent has stopped and logged the decision for audit.")

# ═══════════════════════════════════════════════════════════
st.divider()
st.subheader("🎬 Pattern 3: Escalation Triggers")
st.markdown("""
The agent operates autonomously but **escalates** when it hits uncertainty,
a policy limit, conflicting data, or an action outside its defined authority.
This is the safety net for autonomous agents in production.
""")

st.markdown("**Simulate agent reasoning — edit the thought below:**")
agent_thought = st.text_area(
    "Agent's internal monologue:",
    value="I need to process this customer complaint. They are asking for a refund of $5,000 "
          "which exceeds my $500 auto-approval limit. I also see a previous chargeback dispute "
          "on their account from last year. This situation requires human review.",
    height=120,
    key="agent_thought"
)

ESCALATION_RULES = [
    (["exceed", "limit", "above my authority", "over the threshold"],
     "💰 Amount or action exceeds agent's authority threshold"),
    (["dispute", "chargeback", "legal", "compliance", "regulation"],
     "⚖️ Legal or compliance flag detected"),
    (["uncertain", "unclear", "not sure", "conflicting", "ambiguous"],
     "🤔 Agent confidence below acceptable threshold"),
    (["human", "review", "escalate", "supervisor", "manager"],
     "🙋 Agent self-identified need for human judgment"),
    (["sensitive", "pii", "personal data", "gdpr", "privacy"],
     "🔒 Sensitive data handling requires oversight"),
]

if st.button("🔍 Analyse — Should Agent Escalate?", key="escalate_btn"):
    thought_lower = agent_thought.lower()
    triggers_found = []

    for keywords, label in ESCALATION_RULES:
        if any(kw in thought_lower for kw in keywords):
            triggers_found.append(label)

    if triggers_found:
        st.error("🚨 ESCALATION TRIGGERED — Routing to human supervisor queue")
        for t in triggers_found:
            st.write(f"  • {t}")
        st.info("The agent has paused. A human supervisor will be notified and can take over.")
    else:
        st.success("✅ No escalation triggers detected — agent proceeds autonomously.")

# ═══════════════════════════════════════════════════════════
st.divider()
st.subheader("📚 Key Takeaways")
st.markdown("""
| HITL Pattern | Best For |
|---|---|
| **Risk-Based Gates** | Tasks where risk can be quantified; keeps agent fast for low-risk work |
| **Approval Workflow** | Irreversible, public-facing, or high-value actions |
| **Escalation Triggers** | Autonomous agents that need a safety net for edge cases |

**Real enterprise HITL systems combine all three.** The goal isn't to slow agents down —
it's to place humans in control exactly where it matters most.

---
### 🔗 Continue Learning
- **Previous:** [Module 4 — Agent Security →](./5_Agent_Security_Demo)
- **Foundations:** [GenAI Foundry](https://github.com/dlwhyte/GenAI_foundry) — learn the LLM basics that power these agents
""")
