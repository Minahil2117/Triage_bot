# 🏥 PulseGuard AI • Smart Patient Intake & Triage Pipeline

> **An automated HealthTech pipeline that ingests patient clinical complaints, executes real-time AI triage analysis, generates physician SBAR handoffs, and dispatches multi-channel alerts.**

---

## ⚡ The Automation Architecture

```
                      PULSEGUARD AUTOMATION FLOW
                      
   [Patient Form / Webhook] 
              │
              ▼
    [FastAPI Webhook Receiver]
              │
              ▼
    [Clinical AI Triage Engine] (Analyzes symptoms, red flags, & risk)
              │
     ┌────────┴──────────────────────────┐
     ▼                                   ▼
[Database Persistence]         [Notification Dispatcher]
• SQLite (Audit trail)         • Discord Rich Embeds
• SBAR Physician Notes         • Slack Block Alerts
• Triage Risk Score            • Automated Patient SMS/Email
     │
     ▼
[Clinical Staff Live Dashboard] (Auto-synced Queue & Inspection Modal)
```

---

## 🚀 Key Features

* **Instant Clinical Triage**: Classifies patients into `CRITICAL`, `MEDIUM`, or `LOW` priority with risk scores (1-100) and recommended clinical departments (Emergency Cardiology, Trauma, Urgent Care, Outpatient).
* **Physician SBAR Summary**: Auto-generates structured handoff notes (Situation, Background, Assessment, Recommendation) ready for attending physicians.
* **Dual Engine Flexibility**: Works **100% out-of-the-box** using an intelligent clinical heuristic rule engine, with plug-and-play support for **OpenAI (GPT-4o-mini)** or **Groq (Llama-3.1)**.
* **Multi-Channel Dispatcher**: Automatically pushes rich colored alerts to Discord / Slack webhooks and generates patient instructions.
* **Modern Clinical Dashboard**: Live auto-polling doctor/nurse command center with severity badges, filters, and full case inspection modals.

---

## 🛠 Quickstart Guide

### 1. Requirements Check
The project requires Python 3.10+ and uses standard packages:
```bash
pip install fastapi uvicorn pydantic python-dotenv requests
```

### 2. Run the Application
From inside this directory:
```bash
python main.py
```
*(Or alternatively: `uvicorn main:app --reload --port 8000`)*

### 3. Open in Your Browser
* **Patient Intake Portal:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Clinical Staff Dashboard:** [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)
* **Interactive API Documentation (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

