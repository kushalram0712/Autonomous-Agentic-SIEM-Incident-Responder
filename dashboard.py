import streamlit as st
import requests
import time
import random
import pandas as pd

st.set_page_config(page_title="Next-Gen SIEM SOC Console", layout="wide", initial_sidebar_state="expanded")

# Theme styling override for a high-tech look
st.markdown("""
    <style>
    .metric-card { background-color: #1e272e; padding: 15px; border-radius: 8px; border-left: 5px solid #ff4757; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00d2d3;'>📊 Next-Gen Agentic SIEM & Incident Command Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #84817a;'>Autonomous Detection, Statistical Drift Analytics & AI Remediation Matrix</p>", unsafe_allow_html=True)
st.markdown("---")

BACKEND_URL = "http://localhost:8000"

# Left Sidebar: Attack Controls (Aligned with Assignment Objectives)
st.sidebar.markdown("### 🛠️ Telemetry Exploit Simulator")
attack_vector = st.sidebar.selectbox(
    "Select Target Vector",
    [
        "None",
        "UPI Mule Account Transaction Spike",
        "Android SMS-Forwarding Malware Callback",
        "Vernacular Language Vishing Audio Anomalies",
        "Shadow API Endpoint Harvesting Sweep",
        "Distributed Denial of Service (DDoS) Flood"
    ]
)
trigger_sim = st.sidebar.button("Inject Vector Payload", use_container_width=True)

if trigger_sim:
    st.sidebar.info("Injecting normal baseline stream...")
    for _ in range(12):
        requests.post(f"{BACKEND_URL}/ingest", json={"metric_value": random.uniform(10, 15), "message": "Standard router ingress flow", "vector": "Baseline Traffic"})
        
    if attack_vector == "UPI Mule Account Transaction Spike":
        requests.post(f"{BACKEND_URL}/ingest", json={"metric_value": 240.0, "vector": "UPI Mule Anomaly", "message": "Rapid outbound transaction volume burst on unverified routing layer"})
    elif attack_vector == "Android SMS-Forwarding Malware Callback":
        requests.post(f"{BACKEND_URL}/ingest", json={"metric_value": 98.0, "vector": "Malware C2 Drift", "message": "Suspicious reverse-shell packet burst to external IP mapping on standard ports"})
    elif attack_vector == "Vernacular Language Vishing Audio Anomalies":
        requests.post(f"{BACKEND_URL}/ingest", json={"metric_value": 78.0, "vector": "Hinglish Vishing Audio", "message": "Spike in concurrent audio payload synthesis metrics on localized vernacular gateways"})
    elif attack_vector == "Shadow API Endpoint Harvesting Sweep":
        requests.post(f"{BACKEND_URL}/ingest", json={"metric_value": 110.0, "vector": "Shadow API Scan", "message": "High-velocity directory enumeration scans on unmapped /v3/production gateways"})
    elif attack_vector == "Distributed Denial of Service (DDoS) Flood":
        requests.post(f"{BACKEND_URL}/ingest", json={"metric_value": 350.0, "vector": "DDoS Threat Engine", "message": "Critical packet volume saturation threshold surpassed on edge interface cards"})
        
    st.sidebar.success(f"Stream Active: {attack_vector}")

# Fetch metrics from backend router
try:
    meta = requests.get(f"{BACKEND_URL}/metrics").json()
    total_logs = meta.get("total_logs", 0)
    total_incidents = meta.get("total_incidents", 0)
    incidents_list = requests.get(f"{BACKEND_URL}/incidents").json()
except:
    total_logs, total_incidents, incidents_list = 0, 0, []

# Row 1: Executive KPI Scoreboard Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Total Ingested Log Events", value=total_logs)
with kpi2:
    st.metric(label="Autonomous Incidents Flagged", value=total_incidents, delta=total_incidents, delta_color="inverse")
with kpi3:
    remediated_count = sum(1 for i in incidents_list if i["status"] == "Remediated")
    st.metric(label="AI Self-Healed Threats", value=remediated_count)
with kpi4:
    status_text = "Operational Secure" if total_incidents == 0 else "Active Mitigation Engine"
    st.metric(label="SOC Status", value=status_text)

st.markdown("---")

# Row 2: Tabs for Graphical Analysis vs Real-Time Logs
tab_graph, tab_logs = st.tabs(["📊 Statistical Visualization Matrix", "📋 Real-Time Containment Registry"])

with tab_graph:
    g_col1, g_col2 = st.columns([2, 1])
    with g_col1:
        st.markdown("#### Dynamic Rolling Z-Score Analytics Engine")
        if total_logs > 0:
            # Build a moving timeline chart showing spikes
            chart_vals = [random.uniform(10, 15) for _ in range(max(1, total_logs - len(incidents_list)))]
            for inc in incidents_list:
                chart_vals.append(inc["z_score"] * 10) # Amplify visually for impact
            st.line_chart(pd.DataFrame({"SIEM Metric Baseline Trend": chart_vals}))
    with g_col2:
        st.markdown("#### Threat Breakdown Matrix")
        if incidents_list:
            df = pd.DataFrame(incidents_list)
            st.bar_chart(df["vector"].value_counts())
        else:
            st.info("No threats classified to display distributions yet.")

with tab_logs:
    st.markdown("#### Ingestion Event Registry")
    if incidents_list:
        for inc in reversed(incidents_list):
            is_active = inc["status"] == "Investigating (Agent Loop active)"
            header_color = "🔴 CRITICAL ALERT" if is_active or inc.get("severity") == "CRITICAL" else "🟢 AUTONOMOUS REMEDIATION COMPLETE"
            
            with st.container(border=True):
                sub1, sub2 = st.columns([3, 1])
                with sub1:
                    st.markdown(f"##### {header_color} | Threat ID: #{inc['id']} | Vector: `{inc['vector']}`")
                    st.markdown(f"**Telemetry Message:** `{inc['message']}`")
                    st.markdown(f"🧠 **AI Agent Inference Reasoning:** *{inc['agent_reasoning']}*")
                with sub2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.metric(label="Statistical Z-Score", value=f"{inc['z_score']:.2f}")
                    if is_active:
                        st.info("Agent Deciding...")
                    else:
                        st.success(f"Action Taken:\n{inc['action_taken']}")
    else:
        st.success("Infrastructure environment healthy. No anomalies identified.")

time.sleep(2)
st.rerun()