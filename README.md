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

## 🎬 How to Record a 30-Second LinkedIn Demo Video

1. Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in one half of your screen and **[http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)** in the other half.
2. Click **"🔴 Scenario A: Acute Chest Pain (Critical)"** on the intake form.
3. Click **"Submit Intake & Trigger AI Triage Pipeline"**.
4. Show the instant triage assessment pop up with the **CRITICAL** badge and SBAR note.
5. Switch to the Staff Dashboard and show the patient arriving in real-time in the queue with the red pulse alert!
6. Click **"Inspect SBAR"** to show the doctor handoff.

---

## 📝 LinkedIn Post Template (Copy & Paste to attract recruiters!)

```markdown
🚀 Built an automated AI Patient Intake & Clinical Triage pipeline this weekend!

In healthcare startups and emergency clinics, every second counts. Traditional intake workflows rely on manual triage, leading to backlogs and delayed care for high-risk patients.

To solve this, I engineered PulseGuard AI:
• 🧠 Automated Clinical Triage: Ingests patient symptoms and classifies urgency (Critical, Medium, Routine) with a 1-100 risk score and department routing.
• 🩺 SBAR Handoff Generation: Automatically produces structured Situation-Background-Assessment notes for attending physicians.
• ⚡ Multi-Channel Dispatch: Event-driven webhooks alerting emergency staff via Discord/Slack in sub-seconds.
• 💻 Modern Full-Stack Architecture: Built with FastAPI, Python, SQLite, and a responsive clinical command dashboard.

Check out the 30-second live demo below! 👇

Tech Stack: Python, FastAPI, Webhooks, AI Triage Pipelines, SQLite, Modern Frontend.
#SoftwareEngineering #AIAutomation #HealthTech #FullStack #Python #GenerativeAI
```
