# PROJECT TITLE: Autonomous Agentic SIEM & Incident Responder for Distributed Infrastructure
**Date:** June 30, 2026 | **Author/Lead:** Bezawada Kushal Ram / Intern | [cite_start]**Status:** Completed [cite: 29]
[cite_start]**Project Links:** [https://github.com/kushalram0712/Autonomous-Agentic-SIEM-Incident-Responder](https://github.com/kushalram0712/Autonomous-Agentic-SIEM-Incident-Responder) [cite: 30]

---

## 1. Executive Overview

* [cite_start]**Objective:** To engineer an intelligent, low-latency data pipeline and autonomous incident orchestration engine capable of real-time security telemetry analysis and zero-touch mitigation[cite: 31, 32].
* [cite_start]**The Challenge:** Legacy Security Information and Event Management (SIEM) frameworks depend on static thresholds and introduce substantial cognitive load, causing critical latency delays during rapid exploit cycles[cite: 33, 34].
* [cite_start]**The Solution:** Developed a real-time statistical anomaly detection engine utilizing an auto-calculating rolling $Z$-score algorithm built natively into an asynchronous FastAPI intake microservice[cite: 35]. [cite_start]The alerts are fed directly into a modern Gemini-2.5-Flash LLM autonomous agent loop that dynamically determines and executes precise remediation playbooks[cite: 12, 35].
* [cite_start]**Business Impact:** Eliminated tier-1 manual SOC triage bottlenecks by resolving statistical operational drifts within a <2000ms background execution lifecycle, guaranteeing instant compromise containment[cite: 36].

---

## 2. Technical Architecture & Stack

* [cite_start]**Frontend:** Streamlit Engine (Optimized via HTTP long-polling flags for Google Cloud Shell proxy environments) [cite: 38]
* [cite_start]**Backend / API:** FastAPI, Uvicorn ASGI Web Server [cite: 39]
* **Analytics Engine:** NumPy (Dynamic standard deviation and rolling $Z$-score calculations)
* [cite_start]**Agent Core:** Google GenAI SDK (`gemini-2.5-flash` model executing strict JSON schema constraints) 
* [cite_start]**System Flow:** `[Simulated System Telemetry Stream]` -> `[FastAPI /ingest Endpoint]` -> `[NumPy Real-time Z-Score Evaluator]` -> `[Asynchronous Background Task Controller]` -> `[Gemini LLM Reasoner]` -> `[Automated Playbook Execution Matrix]` -> `[Streamlit State Rerender]` 

---

## 3. Key Deliverables & Features

* [cite_start]**Statistical Drift Engine:** Computes immediate mathematical deviations dynamically across incoming telemetry streams to pinpoint behavioral shifts without relying on fragile, hardcoded rule sets[cite: 44].
* [cite_start]**Agentic Orchestration Logic:** An asynchronous worker using the modern `google-genai` client that interprets raw alert telemetry and chooses optimized containment configurations[cite: 12, 45].
* [cite_start]**Zero-Touch Remediation Interface:** An interactive operations console displaying live metric baselines, color-coded threat statuses, and real-time AI cognitive reasoning strings[cite: 46].

---

## 4. Implementation Highlights & Performance

* [cite_start]**Security & Compliance:** Built strictly around passive telemetry data ingestion, completely avoiding interaction with illicit resources or storage of dangerous components to ensure safe adherence to project constraints[cite: 16, 17, 48].
* [cite_start]**Performance Metrics:** The backend evaluation engine tracks metrics and calculates standard deviations in under 50ms, safely allowing the background agent process to handle remediation asynchronously without locking the primary ingestion path[cite: 49].
* [cite_start]**Quality Assurance:** Maintained structured development workflows and complete verification loops across components to ensure zero runtime conflicts under high stress conditions[cite: 50].

---

## 5. Challenges & Strategic Roadmap

* **Primary Technical Hurdle:** Bypassing standard WebSocket connection drops caused by Google Cloud Shell web proxy wrappers during high-frequency frontend updates.
* **Resolution:** Re-configured the dashboard framework to leverage explicit proxy bypass parameters (`--server.enableWebsocketCompression false`) and established long-polling data loops.
* **Next Steps (Phase 2):**
  * Integrate an SQLite database layer to maintain a persistent baseline of historical logs across server reboots.
  * Connect the outputted JSON response to local bash sub-processes to automatically trigger local environment container isolation commands.
