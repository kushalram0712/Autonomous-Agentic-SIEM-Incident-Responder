from fastapi import FastAPI, BackgroundTasks
import numpy as np
from google import genai
import json
import os
import time

app = FastAPI(title="Enterprise Agentic SIEM Engine")
client = genai.Client()

log_history = []
incidents = []

def call_agentic_llm_responder(incident_id: int, log_data: dict, score: float):
    try:
        prompt = f"""
        You are an Autonomous Incident Response AI Agent operating inside an Enterprise Zero-Touch SOC.
        An operational telemetry drift has occurred with a critical Z-Score of {score:.2f}.
        
        LOG DATA ENCOUNTERED:
        {json.dumps(log_data)}
        
        CRITICAL TASK:
        Analyze the log data and select the absolute best mitigation response out of these five choices:
        1. "IP temporarily blocked via Cloud Firewall rule." (Use for Brute Force/Auth Abuse)
        2. "Isolated compromised microservice container." (Use for massive Data Exfiltration or Malware callbacks)
        3. "Rate-limiting policy applied to API Gateway." (Use for DDoS or Shadow API scanning loops)
        4. "Suspended target endpoint router / UPI account flags." (Use for financial transaction volume anomalies)
        5. "Flagged for manual SOC tier-2 investigation." (Use for ambiguous anomalies)
        
        OUTPUT FORMAT CONSTRAINT:
        You must reply STRICTLY with a valid JSON object. Do not include markdown code blocks or extra text.
        
        Expected JSON Schema structure:
        {{
            "reasoning": "Your brief architectural explanation here",
            "action_chosen": "Exact string matching one of the five choices above",
            "threat_severity": "HIGH" or "CRITICAL"
        }}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        result = json.loads(clean_text)
        
        action = result.get("action_chosen", "Flagged for manual SOC tier-2 investigation.")
        reasoning = result.get("reasoning", "Fallback mitigation triggered.")
        severity = result.get("threat_severity", "HIGH")
        
    except Exception as e:
        action = "Flagged for manual SOC tier-2 investigation."
        reasoning = f"Fallback triggered due to agent exception error: {str(e)}"
        severity = "HIGH"

    for inc in incidents:
        if inc["id"] == incident_id:
            inc["status"] = "Remediated"
            inc["action_taken"] = action
            inc["agent_reasoning"] = reasoning
            inc["severity"] = severity
            break

@app.post("/ingest")
def ingest_log(log: dict, background_tasks: BackgroundTasks):
    global log_history
    metric_value = log.get("metric_value", 1.0)
    log_history.append(metric_value)
    
    status = "Normal"
    if len(log_history) > 10:
        recent_history = log_history[-30:]
        mean = np.mean(recent_history[:-1])
        std = np.std(recent_history[:-1]) + 1e-5
        z_score = abs((metric_value - mean) / std)
        
        if z_score > 2.5:
            status = "Anomaly Detected"
            incident_id = len(incidents) + 1
            incident_data = {
                "id": incident_id,
                "timestamp": log.get("timestamp", time.time()),
                "message": log.get("message", "Unknown anomaly"),
                "vector": log.get("vector", "General Anomaly"),
                "z_score": float(z_score),
                "status": "Investigating (Agent Loop active)",
                "action_taken": "Pending",
                "agent_reasoning": "Awaiting agent validation...",
                "severity": "PENDING"
            }
            incidents.append(incident_data)
            background_tasks.add_task(call_agentic_llm_responder, incident_id, log, z_score)

    return {"status": "Success", "log_evaluation": status}

@app.get("/incidents")
def get_incidents():
    return incidents

@app.get("/metrics")
def get_metrics():
    return {"total_logs": len(log_history), "total_incidents": len(incidents)}