"""
PulseGuard AI Triage Bot - FastAPI Server
Entrypoint for the automated intake, triage, and notification pipeline.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os

from database import init_db, save_patient, get_patients, get_patient_by_id, get_stats
from triage_engine import run_triage
from notifier import dispatch_all

app = FastAPI(
    title="PulseGuard AI - HealthTech Triage Pipeline",
    description="Automated Patient Intake, Clinical Triage, and Dispatch Automation",
    version="1.0.0"
)

# Mount static assets
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class IntakeRequest(BaseModel):
    full_name: str = Field(..., example="Eleanor Vance")
    age: int = Field(..., ge=0, le=120, example=45)
    gender: str = Field(..., example="Female")
    contact_email: Optional[str] = Field(None, example="eleanor@example.com")
    contact_phone: Optional[str] = Field(None, example="+1 (555) 234-5678")
    chief_complaint: str = Field(..., example="Acute pressure in chest with left arm numbness")
    symptoms_detail: str = Field(..., example="Began 45 minutes ago while resting. Feels like a tight band across chest. Cold sweat and dizziness.")
    duration: Optional[str] = Field("Under 1 hour", example="45 minutes")
    pre_existing_conditions: Optional[str] = Field("None", example="Hypertension, Type 2 Diabetes")

@app.on_event("startup")
def on_startup():
    init_db()
    # Check if DB is empty; if so, populate 3 realistic demo cases
    stats = get_stats()
    if stats["total"] == 0:
        seed_demo_data()

def seed_demo_data():
    demos = [
        {
            "full_name": "Marcus Aurelius Reed",
            "age": 62,
            "gender": "Male",
            "contact_email": "m.reed@example.com",
            "contact_phone": "+1 (555) 019-2831",
            "chief_complaint": "Crushing chest pain radiating to jaw with cold sweats",
            "symptoms_detail": "Sudden onset 30 mins ago. Feels like intense pressure, difficulty catching breath, nausea and sweating.",
            "duration": "30 minutes",
            "pre_existing_conditions": "Hypertension, Hyperlipidemia"
        },
        {
            "full_name": "Sophia Zhang",
            "age": 28,
            "gender": "Female",
            "contact_email": "sophia.z@example.com",
            "contact_phone": "+1 (555) 304-9182",
            "chief_complaint": "Persistent high fever and productive cough for 3 days",
            "symptoms_detail": "Temperature 102.5 F for 3 days. Deep cough with green sputum, body fatigue, chills, unable to keep fluids down today.",
            "duration": "3 days",
            "pre_existing_conditions": "None"
        },
        {
            "full_name": "Liam Connor",
            "age": 34,
            "gender": "Male",
            "contact_email": "liam.c@example.com",
            "contact_phone": "+1 (555) 881-2041",
            "chief_complaint": "Mild skin rash on forearm with minor itching",
            "symptoms_detail": "Red circular patch appeared yesterday after gardening. No pain, no systemic symptoms, no breathing issues.",
            "duration": "24 hours",
            "pre_existing_conditions": "Seasonal allergies"
        }
    ]
    for d in demos:
        assessment = run_triage(d)
        record = {**d, **assessment}
        save_patient(record)

@app.get("/")
def serve_patient_portal():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/dashboard")
def serve_clinical_dashboard():
    return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

@app.post("/api/intake")
def process_patient_intake(intake: IntakeRequest):
    """
    Main webhook / intake endpoint:
    1. Runs clinical AI triage
    2. Saves record to SQLite
    3. Dispatches multi-channel notifications (Discord/Slack/Console)
    """
    data = intake.model_dump()
    
    # 1. AI Triage Pipeline
    assessment = run_triage(data)
    
    # 2. Database Persistence
    full_record = {**data, **assessment}
    patient_id = save_patient(full_record)
    
    # 3. Automated Notification Dispatch
    dispatch_results = dispatch_all(patient_id, assessment, data)
    
    return {
        "status": "success",
        "patient_id": patient_id,
        "assessment": assessment,
        "dispatch": dispatch_results
    }

@app.get("/api/patients")
def list_patients(urgency: Optional[str] = Query("ALL", description="Filter by ALL, CRITICAL, MEDIUM, LOW")):
    patients = get_patients(urgency_filter=urgency)
    return {"patients": patients, "count": len(patients)}

@app.get("/api/patients/{patient_id}")
def patient_details(patient_id: str):
    patient = get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")
    return patient

@app.get("/api/stats")
def clinic_stats():
    return get_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
