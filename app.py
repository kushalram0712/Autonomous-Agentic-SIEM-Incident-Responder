from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.orm import Session
import numpy as np
from google import genai
import json
import os
import time

import database as db

app = FastAPI(title="Production Agentic SIEM Engine")
client = genai.Client()

# Dependency to get the DB session
def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

def call_agentic_llm_responder(incident_id: int, log_data: dict, score: float):
    session = db.SessionLocal()
    try:
        prompt = f"""
        You are an Autonomous Incident Response AI Agent operating inside an Enterprise Zero-Touch SOC.
        An operational telemetry drift has occurred with a critical Z-Score of {score:.2f}.
        
        LOG DATA ENCOUNTERED:
        {json.dumps(log_data)}
        
        CRITICAL TASK:
        Analyze the log data and select the absolute best mitigation response out of these five choices:
        1. "IP temporarily blocked via Cloud Firewall rule."
        2. "Isolated compromised microservice container."
        3. "Rate-limiting policy applied to API Gateway."
        4. "Suspended target endpoint router / UPI account flags."
        5. "Flagged for manual SOC tier-2 investigation."
        
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

    # Persist the remediation metrics back to SQLite
    inc = session.query(db.IncidentRecord).filter(db.IncidentRecord.id == incident_id).first()
    if inc:
        inc.status = "Remediated"
        inc.action_taken = action
        inc.agent_reasoning = reasoning
        inc.severity = severity
        session.commit()
    session.close()

@app.post("/ingest")
def ingest_log(log: dict, background_tasks: BackgroundTasks, session: Session = Depends(get_db)):
    metric_value = log.get("metric_value", 1.0)
    
    # Save raw log entry to DB
    new_log = db.LogEntry(
        metric_value=metric_value,
        message=log.get("message", "Standard Log"),
        vector=log.get("vector", "Baseline")
    )
    session.add(new_log)
    session.commit()
    
    # Extract baseline from DB for dynamic Z-score calculation
    all_logs = session.query(db.LogEntry.metric_value).order_by(db.LogEntry.id.desc()).limit(30).all()
    log_values = [l[0] for l in all_logs]
    
    status = "Normal"
    if len(log_values) > 10:
        mean = np.mean(log_values[1:])
        std = np.std(log_values[1:]) + 1e-5
        z_score = abs((metric_value - mean) / std)
        
        if z_score > 2.5:
            status = "Anomaly Detected"
            new_incident = db.IncidentRecord(
                timestamp=time.time(),
                message=log.get("message", "Unknown Anomaly"),
                vector=log.get("vector", "General Anomaly"),
                z_score=float(z_score),
                status="Investigating (Agent Loop active)",
                action_taken="Pending",
                agent_reasoning="Awaiting validation configuration...",
                severity="PENDING"
            )
            session.add(new_incident)
            session.commit()
            
            # Pass back to background agent threads
            background_tasks.add_task(call_agentic_llm_responder, new_incident.id, log, z_score)

    return {"status": "Success", "log_evaluation": status}

@app.get("/incidents")
def get_incidents(session: Session = Depends(get_db)):
    return session.query(db.IncidentRecord).all()

@app.get("/metrics")
def get_metrics(session: Session = Depends(get_db)):
    total_logs = session.query(db.LogEntry).count()
    total_incidents = session.query(db.IncidentRecord).count()
    return {"total_logs": total_logs, "total_incidents": total_incidents}