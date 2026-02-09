"""
MCP Explorer - Understanding the Model Context Protocol
=======================================================

An interactive tool that helps you understand how MCP works
by walking through real-world scenarios step by step.

Key Concepts:
- How MCP standardizes AI-to-tool communication
- The difference between MCP, custom APIs, and automation tools
- How MCP messages flow between AI models and servers

No API key required - this is a simulation/educational tool.
"""

import streamlit as st
import json
import time

# ─────────────────────────────────────────────
# MCP SCENARIO DEFINITIONS
# ─────────────────────────────────────────────

MCP_SCENARIOS = {
    "📅 Schedule a Meeting": {
        "user_request": "Schedule a meeting with Sarah for next Tuesday at 2pm",
        "steps": [
            {
                "component": "User",
                "action": "Sends natural language request",
                "detail": "\"Schedule a meeting with Sarah for next Tuesday at 2pm\"",
                "color": "#718096",
            },
            {
                "component": "AI Model",
                "action": "Parses intent and extracts parameters",
                "detail": "Identifies: action=schedule_meeting, contact=Sarah, date=next_tuesday, time=14:00",
                "color": "#0F2B46",
            },
            {
                "component": "MCP Client",
                "action": "Discovers available MCP servers",
                "detail": "Queries registry → finds 'google_calendar' and 'outlook_calendar' servers",
                "color": "#065A82",
                "json_message": {
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "id": 1
                },
                "json_response": {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "result": {
                        "tools": [
                            {"name": "create_event", "description": "Create a calendar event"},
                            {"name": "check_availability", "description": "Check calendar availability"},
                            {"name": "list_events", "description": "List upcoming events"}
                        ]
                    }
                }
            },
            {
                "component": "MCP Protocol",
                "action": "Sends standardized JSON-RPC request to calendar server",
                "detail": "Uses tools/call with create_event tool and structured parameters",
                "color": "#1C7293",
                "json_message": {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "create_event",
                        "arguments": {
                            "title": "Meeting with Sarah",
                            "date": "2026-02-17",
                            "time": "14:00",
                            "duration_minutes": 30,
                            "attendees": ["sarah@company.com"]
                        }
                    },
                    "id": 2
                }
            },
            {
                "component": "Calendar Server",
                "action": "Checks availability and creates the event",
                "detail": "Verifies Sarah is free at 2pm, creates event, sends calendar invite",
                "color": "#065A82",
                "json_response": {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": "Event created: 'Meeting with Sarah' on Tue Feb 17 at 2:00 PM. Calendar invite sent."
                        }],
                        "isError": False
                    }
                }
            },
            {
                "component": "AI Model",
                "action": "Formats confirmation for user",
                "detail": "Translates structured response back to natural language",
                "color": "#0F2B46",
            },
            {
                "component": "User",
                "action": "Receives confirmation",
                "detail": "\"Done — meeting with Sarah scheduled for Tuesday at 2pm. Calendar invite sent.\"",
                "color": "#718096",
            },
        ],
    },
    "🎵 Spotify Playlist": {
        "user_request": "Make me a birthday playlist with #1 Billboard hits from every year since 1985",
        "steps": [
            {
                "component": "User",
                "action": "Sends natural language request",
                "detail": "\"Make me a birthday playlist with #1 hits from every year since 1985\"",
                "color": "#718096",
            },
            {
                "component": "AI Model",
                "action": "Decomposes into multi-step plan",
                "detail": "Plan: (1) search Billboard data, (2) match to Spotify catalog, (3) create playlist, (4) add tracks",
                "color": "#0F2B46",
            },
            {
                "component": "MCP Client",
                "action": "Discovers required MCP servers",
                "detail": "Finds 'web_search' server for Billboard data and 'spotify' server for playlist management",
                "color": "#065A82",
                "json_message": {
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "id": 1
                }
            },
            {
                "component": "MCP Protocol → Web Search",
                "action": "Retrieves Billboard #1 hits for each year",
                "detail": "Queries web search MCP server for chart data (1985-2025)",
                "color": "#1C7293",
                "json_message": {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "web_search",
                        "arguments": {
                            "query": "Billboard Hot 100 #1 songs by year 1985-2025"
                        }
                    },
                    "id": 2
                }
            },
            {
                "component": "MCP Protocol → Spotify",
                "action": "Creates playlist and searches for tracks",
                "detail": "Creates empty playlist, then searches Spotify catalog for each song",
                "color": "#1C7293",
                "json_message": {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "create_playlist",
                        "arguments": {
                            "name": "Birthday Hits 1985-2025",
                            "description": "#1 Billboard hits from every year",
                            "public": False
                        }
                    },
                    "id": 3
                }
            },
            {
                "component": "Spotify Server",
                "action": "Matches songs, creates playlist, adds tracks",
                "detail": "40 tracks matched and added. 2 songs not found in catalog — flagged for user.",
                "color": "#065A82",
                "json_response": {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": "Playlist 'Birthday Hits 1985-2025' created with 38/40 tracks. 2 songs unavailable in your region."
                        }]
                    }
                }
            },
            {
                "component": "AI Model",
                "action": "Summarizes and reports",
                "detail": "Provides link, track count, and notes which songs couldn't be found",
                "color": "#0F2B46",
            },
            {
                "component": "User",
                "action": "Receives result",
                "detail": "\"Your playlist 'Birthday Hits 1985-2025' is ready! 38 songs added. 2 tracks weren't available in your region — would you like alternatives?\"",
                "color": "#718096",
            },
        ],
    },
    "🔍 Salesforce CRM Lookup": {
        "user_request": "What's the status of the Acme Corp deal and when did we last contact them?",
        "steps": [
            {
                "component": "User",
                "action": "Asks about a customer account",
                "detail": "\"What's the status of the Acme Corp deal and when did we last contact them?\"",
                "color": "#718096",
            },
            {
                "component": "AI Model",
                "action": "Identifies two data needs",
                "detail": "Need: (1) opportunity/deal status for Acme Corp, (2) last activity/contact date",
                "color": "#0F2B46",
            },
            {
                "component": "MCP Client",
                "action": "Routes to Salesforce MCP server",
                "detail": "Discovers 'salesforce' MCP server with CRM query capabilities",
                "color": "#065A82",
            },
            {
                "component": "MCP Protocol",
                "action": "Queries opportunity and activity records",
                "detail": "Two sequential tool calls: search_opportunity + get_activities",
                "color": "#1C7293",
                "json_message": {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "search_opportunities",
                        "arguments": {
                            "account_name": "Acme Corp",
                            "fields": ["StageName", "Amount", "CloseDate", "LastActivityDate"]
                        }
                    },
                    "id": 2
                }
            },
            {
                "component": "Salesforce Server",
                "action": "Returns structured CRM data",
                "detail": "Opportunity found: Negotiation stage, $450K, expected close March 15",
                "color": "#065A82",
                "json_response": {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": "Opportunity: 'Acme Corp Enterprise License' | Stage: Negotiation/Review | Amount: $450,000 | Expected Close: 2026-03-15 | Last Activity: Email from Sarah Chen on 2026-02-05"
                        }]
                    }
                }
            },
            {
                "component": "AI Model",
                "action": "Synthesizes and presents findings",
                "detail": "Combines deal status + last contact into a clear summary",
                "color": "#0F2B46",
            },
            {
                "component": "User",
                "action": "Gets actionable summary",
                "detail": "\"The Acme Corp deal ($450K) is in Negotiation. Sarah Chen last emailed them on Feb 5. Expected close: March 15. Want me to draft a follow-up?\"",
                "color": "#718096",
            },
        ],
    },
    "📊 DevOps Alert Triage": {
        "user_request": "We're getting alerts on the payment service — what's going on?",
        "steps": [
            {
                "component": "User",
                "action": "Reports an alert in Slack",
                "detail": "\"We're getting alerts on the payment service — what's going on?\"",
                "color": "#718096",
            },
            {
                "component": "AI Model",
                "action": "Plans diagnostic sequence",
                "detail": "Plan: (1) check monitoring dashboard, (2) read recent logs, (3) check deployment history",
                "color": "#0F2B46",
            },
            {
                "component": "MCP Client",
                "action": "Discovers monitoring and logging servers",
                "detail": "Finds 'datadog' MCP server for metrics and 'github' server for deployment history",
                "color": "#065A82",
            },
            {
                "component": "MCP Protocol → Datadog",
                "action": "Queries service metrics and alerts",
                "detail": "Fetches error rate, latency, and active alerts for payment-service",
                "color": "#1C7293",
                "json_message": {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "get_service_metrics",
                        "arguments": {
                            "service": "payment-service",
                            "metrics": ["error_rate", "p99_latency", "request_count"],
                            "timeframe": "last_1h"
                        }
                    },
                    "id": 2
                },
                "json_response": {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": "payment-service: error_rate=12.4% (normal: <1%), p99_latency=3200ms (normal: 200ms), request_count=stable. Alert: 'High Error Rate' triggered 18 min ago."
                        }]
                    }
                }
            },
            {
                "component": "MCP Protocol → GitHub",
                "action": "Checks recent deployments",
                "detail": "Queries deployment history to correlate with alert timing",
                "color": "#1C7293",
                "json_message": {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "list_deployments",
                        "arguments": {
                            "repo": "company/payment-service",
                            "timeframe": "last_2h"
                        }
                    },
                    "id": 3
                },
                "json_response": {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": "Deployment: v2.14.3 deployed 22 min ago by @mike. Changes: updated Stripe SDK, modified retry logic."
                        }]
                    }
                }
            },
            {
                "component": "AI Model",
                "action": "Correlates data and diagnoses",
                "detail": "Deployment 22 min ago → alerts 18 min ago. Stripe SDK update likely cause.",
                "color": "#0F2B46",
            },
            {
                "component": "User",
                "action": "Gets diagnosis and recommendation",
                "detail": "\"Error rate spiked to 12.4% starting ~18 min ago, right after v2.14.3 was deployed (Stripe SDK update by @mike). Recommend: rollback to v2.14.2. Want me to trigger it?\"",
                "color": "#718096",
            },
        ],
    },
}

COMPARISON_DATA = {
    "Connect Gmail to Slack when a VIP customer emails": {
        "zapier": {
            "approach": "Trigger/Action workflow",
            "steps": [
                "1. Trigger: New email in Gmail matching filter",
                "2. Filter: Check if sender is in VIP list",
                "3. Action: Send Slack message to #vip-alerts",
            ],
            "pros": "No code, setup in minutes",
            "cons": "No AI reasoning — just pattern matching. Can't understand email content or adapt.",
            "ai_aware": False,
        },
        "custom_api": {
            "approach": "Custom Python script + API calls",
            "steps": [
                "1. Gmail API: watch for new emails (OAuth setup)",
                "2. Custom logic: parse sender, check VIP database",
                "3. NLP model: classify urgency (optional)",
                "4. Slack API: post message with formatting",
                "5. Error handling, retry logic, logging",
            ],
            "pros": "Full control, can add AI classification",
            "cons": "Requires developer, OAuth management, error handling, deployment infrastructure.",
            "ai_aware": False,
        },
        "mcp": {
            "approach": "AI agent with Gmail + Slack MCP servers",
            "steps": [
                "1. Agent receives: 'Monitor VIP emails'",
                "2. Discovers Gmail MCP server → watches inbox",
                "3. AI reads and understands the email content",
                "4. Decides urgency, drafts context-aware summary",
                "5. Discovers Slack MCP server → posts to appropriate channel",
            ],
            "pros": "AI understands content, adapts behavior, can handle follow-ups. One protocol for both tools.",
            "cons": "Newer ecosystem, fewer pre-built MCP servers (but growing fast).",
            "ai_aware": True,
        },
    },
    "Pull weekly sales data and generate a report": {
        "zapier": {
            "approach": "Scheduled trigger + data formatting",
            "steps": [
                "1. Trigger: Every Monday at 9am",
                "2. Action: Pull data from Salesforce/HubSpot",
                "3. Action: Format into Google Sheet",
                "4. Action: Email the sheet",
            ],
            "pros": "Reliable, scheduled, no code",
            "cons": "Static format. Can't analyze trends, spot anomalies, or write narrative insights.",
            "ai_aware": False,
        },
        "custom_api": {
            "approach": "Python script with CRM API + reporting",
            "steps": [
                "1. Salesforce API: SOQL query for weekly data",
                "2. Pandas: data processing and aggregation",
                "3. Matplotlib/Plotly: generate charts",
                "4. Jinja2: render HTML report template",
                "5. SMTP: email the report",
            ],
            "pros": "Custom visualizations, any data transformation",
            "cons": "Maintenance burden. Template changes require code changes. No narrative analysis.",
            "ai_aware": False,
        },
        "mcp": {
            "approach": "AI agent with CRM + document MCP servers",
            "steps": [
                "1. Agent runs weekly: 'Generate sales report'",
                "2. Queries Salesforce MCP server for metrics",
                "3. AI analyzes: spots trends, anomalies, comparisons",
                "4. Writes narrative summary with data-driven insights",
                "5. Sends via email MCP server with charts and commentary",
            ],
            "pros": "AI writes analysis, spots anomalies humans miss, adapts format to audience.",
            "cons": "Needs well-structured MCP servers for your specific CRM.",
            "ai_aware": True,
        },
    },
}


# ─────────────────────────────────────────────
# STREAMLIT APP
# ─────────────────────────────────────────────

def render_json_block(label, data):
    """Render a formatted JSON block."""
    st.markdown(f"**{label}:**")
    st.code(json.dumps(data, indent=2), language="json")


def render_step_animated(step, step_num, total_steps, animate=True):
    """Render a single MCP step with styling."""
    is_user = step["component"] == "User"
    is_ai = step["component"] == "AI Model"

    # Component badge color
    bg = step["color"]

    st.markdown(f"""
    <div style="display: flex; align-items: flex-start; margin-bottom: 0.8rem; gap: 0.8rem;">
        <div style="min-width: 140px; background: {bg}; color: white; padding: 0.4rem 0.7rem; 
                    border-radius: 6px; font-size: 0.8rem; font-weight: 600; text-align: center;">
            {step["component"]}
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 0.2rem;">{step["action"]}</div>
            <div style="color: #4a5568; font-size: 0.9rem;">{step["detail"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Show JSON messages if present
    col1, col2 = st.columns(2)
    if "json_message" in step:
        with col1:
            render_json_block("📤 MCP Request", step["json_message"])
    if "json_response" in step:
        with (col2 if "json_message" in step else col1):
            render_json_block("📥 MCP Response", step["json_response"])


def main():
    st.set_page_config(
        page_title="MCP Explorer",
        page_icon="🔌",
        layout="wide",
    )

    # Custom CSS
    st.markdown("""
    <style>
        .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A5F; margin-bottom: 0.3rem; }
        .sub-header { font-size: 1.1rem; color: #666; margin-bottom: 1.5rem; }
        .insight-box {
            background: linear-gradient(135deg, #065A82 0%, #1C7293 100%);
            color: white; padding: 1.2rem; border-radius: 10px; margin: 1rem 0;
        }
        .card { background: #f8f9fa; border-radius: 10px; padding: 1.2rem; margin-bottom: 0.8rem; border-left: 4px solid #1C7293; }
        .compare-header { font-size: 1rem; font-weight: 700; padding: 0.5rem; border-radius: 6px; text-align: center; color: white; margin-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-header">🔌 MCP Explorer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Understanding the Model Context Protocol — how AI agents connect to business tools</p>', unsafe_allow_html=True)

    # Key insight
    st.markdown("""
    <div class="insight-box">
        <h4 style="margin-top:0;">🔑 The USB-C Analogy</h4>
        <p style="font-size: 1.1rem; margin-bottom: 0;">
        Before USB-C, every device needed a different cable. Before MCP, every AI + tool pairing needed a custom integration.<br/>
        <strong>MCP is USB-C for AI</strong> — one standard protocol that lets any AI model talk to any tool.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🎬 Step-by-Step Scenarios", "⚖️ MCP vs. Alternatives", "📘 How MCP Works"])

    # ─── TAB 1: Scenarios ───
    with tab1:
        st.markdown("### Walk Through a Real MCP Interaction")
        st.markdown("Select a scenario to see exactly how an AI agent uses MCP to complete a task — every protocol message, every server response.")

        scenario_name = st.selectbox(
            "Choose a scenario:",
            list(MCP_SCENARIOS.keys()),
            index=0,
        )

        scenario = MCP_SCENARIOS[scenario_name]

        st.markdown(f"""
        <div style="background: #D4EEF7; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #1C7293;">
            <strong>User Request:</strong> "{scenario['user_request']}"
        </div>
        """, unsafe_allow_html=True)

        animate = st.checkbox("⏱️ Animate steps (show one at a time)", value=False)

        if animate:
            placeholder = st.empty()
            for i, step in enumerate(scenario["steps"]):
                with placeholder.container():
                    st.markdown(f"**Step {i+1} of {len(scenario['steps'])}**")
                    render_step_animated(step, i, len(scenario["steps"]), animate=False)
                    st.progress((i + 1) / len(scenario["steps"]))
                time.sleep(1.5)
            # Show all at end
            placeholder.empty()

        st.markdown("---")
        st.markdown("#### Full Interaction Flow")
        for i, step in enumerate(scenario["steps"]):
            render_step_animated(step, i, len(scenario["steps"]), animate=False)
            if i < len(scenario["steps"]) - 1:
                st.markdown("<div style='text-align: center; color: #aaa; font-size: 1.2rem;'>↓</div>", unsafe_allow_html=True)

        # Takeaway
        st.markdown("""
        <div style="background: #FFF3D6; padding: 1rem; border-radius: 8px; margin-top: 1.5rem; border-left: 4px solid #E8A838;">
            <strong>💡 Key Takeaway:</strong> The user never writes JSON or calls APIs. 
            They speak naturally, and MCP handles the translation between AI intent and tool execution.
        </div>
        """, unsafe_allow_html=True)

    # ─── TAB 2: Compare ───
    with tab2:
        st.markdown("### Same Task, Three Approaches")
        st.markdown("See how the same integration task looks with Zapier, custom APIs, and MCP.")

        task_name = st.selectbox(
            "Choose a task:",
            list(COMPARISON_DATA.keys()),
            index=0,
        )

        task = COMPARISON_DATA[task_name]

        col1, col2, col3 = st.columns(3)

        for col, (approach, data), color in zip(
            [col1, col2, col3],
            [("Zapier / n8n", task["zapier"]), ("Custom APIs", task["custom_api"]), ("MCP", task["mcp"])],
            ["#718096", "#C53030", "#065A82"],
        ):
            with col:
                st.markdown(f'<div class="compare-header" style="background: {color};">{approach}</div>', unsafe_allow_html=True)
                st.markdown(f"**Approach:** {data['approach']}")
                st.markdown("**Steps:**")
                for step in data["steps"]:
                    st.markdown(f"<span style='font-size:0.9rem;'>{step}</span>", unsafe_allow_html=True)
                st.markdown(f"✅ **Pros:** {data['pros']}")
                st.markdown(f"⚠️ **Cons:** {data['cons']}")
                ai_badge = "🧠 AI-Aware" if data["ai_aware"] else "🔧 Rule-Based"
                badge_color = "#065A82" if data["ai_aware"] else "#718096"
                st.markdown(f'<span style="background:{badge_color}; color:white; padding:0.2rem 0.6rem; border-radius:12px; font-size:0.8rem;">{ai_badge}</span>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div class="insight-box">
            <h4 style="margin-top:0;">📋 For Your Assignment (Q3: Integration)</h4>
            <p>When answering "How would it integrate with existing systems?" — don't just say "APIs."<br/>
            Name the specific approach (Zapier, MCP, custom API) and explain <strong>why</strong> it fits your org's technical maturity.</p>
        </div>
        """, unsafe_allow_html=True)

    # ─── TAB 3: How MCP Works ───
    with tab3:
        st.markdown("### The Three Layers of MCP")

        layers = [
            ("🧠 AI Model (MCP Client)", "#0F2B46",
             "The AI model (Claude, GPT, Gemini, etc.) that receives user requests and decides which tools to use.",
             ["Parses natural language into structured intent", "Decides which MCP tools to call and in what order", "Interprets results and responds to the user"]),
            ("📡 MCP Protocol Layer", "#065A82",
             "The standardized communication protocol — JSON-RPC 2.0 messages with defined methods.",
             ["tools/list — discover available tools", "tools/call — invoke a specific tool with parameters", "resources/read — access data sources", "prompts/get — retrieve prompt templates"]),
            ("🔧 MCP Servers (Tools)", "#1C7293",
             "External services wrapped in a standard MCP interface. Each server exposes tools the AI can call.",
             ["Google Calendar, Slack, Salesforce, GitHub, Spotify...", "Each server handles auth, rate limiting, and error handling internally", "New servers can be added without changing the AI model"]),
        ]

        for name, color, desc, bullets in layers:
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <h4 style="margin: 0; color: white;">{name}</h4>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(desc)
            for b in bullets:
                st.markdown(f"- {b}")
            st.markdown("")

        st.markdown("---")
        st.markdown("### Why This Matters")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card">
            <h4>Without MCP</h4>
            <p>10 AI models × 10 tools = <strong>100 custom integrations</strong></p>
            <p>Each one needs its own auth handling, error logic, data formatting, and maintenance.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="card" style="border-left-color: #2F855A;">
            <h4>With MCP</h4>
            <p>10 AI models + 10 tools = <strong>20 standard connections</strong></p>
            <p>Each AI implements one client. Each tool implements one server. They all speak the same language.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### MCP Message Anatomy")
        st.markdown("Every MCP interaction uses **JSON-RPC 2.0**. Here's what a typical tool call looks like:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📤 Request (AI → Server)**")
            st.code(json.dumps({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "send_message",
                    "arguments": {
                        "channel": "#general",
                        "text": "Weekly report is ready"
                    }
                },
                "id": 1
            }, indent=2), language="json")

        with col2:
            st.markdown("**📥 Response (Server → AI)**")
            st.code(json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": "Message sent to #general at 9:05 AM"
                    }],
                    "isError": False
                }
            }, indent=2), language="json")

    # ─── Footer ───
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <strong>MCP Explorer</strong> | Part of AgenticAI Foundry | Module 3: Agent Design & Integration<br>
        No API key required — educational simulation
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
