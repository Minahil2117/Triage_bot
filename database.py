"""
Database layer for PulseGuard AI Triage Bot
Uses SQLite to store patient intakes, triage assessments, and dispatch logs.
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any

DB_PATH = "triage.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        full_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        contact_email TEXT,
        contact_phone TEXT,
        chief_complaint TEXT NOT NULL,
        symptoms_detail TEXT NOT NULL,
        duration TEXT,
        pre_existing_conditions TEXT,
        urgency TEXT NOT NULL,
        urgency_score INTEGER NOT NULL,
        department TEXT NOT NULL,
        clinical_rationale TEXT NOT NULL,
        physician_summary TEXT NOT NULL,
        patient_message TEXT NOT NULL,
        notification_status TEXT DEFAULT 'DISPATCHED'
    )
    """)
    conn.commit()
    conn.close()

def save_patient(record: Dict[str, Any]) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    
    # Generate unique ID if not provided
    patient_id = record.get("id") or f"PT-{uuid.uuid4().hex[:6].upper()}"
    
    cursor.execute("""
    INSERT INTO patients (
        id, full_name, age, gender, contact_email, contact_phone,
        chief_complaint, symptoms_detail, duration, pre_existing_conditions,
        urgency, urgency_score, department, clinical_rationale,
        physician_summary, patient_message, notification_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        record["full_name"],
        record["age"],
        record["gender"],
        record.get("contact_email", ""),
        record.get("contact_phone", ""),
        record["chief_complaint"],
        record["symptoms_detail"],
        record.get("duration", "Not specified"),
        record.get("pre_existing_conditions", "None reported"),
        record["urgency"],
        record["urgency_score"],
        record["department"],
        record["clinical_rationale"],
        record["physician_summary"],
        record["patient_message"],
        record.get("notification_status", "DISPATCHED")
    ))
    conn.commit()
    conn.close()
    return patient_id

def get_patients(urgency_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    
    if urgency_filter and urgency_filter.upper() != "ALL":
        cursor.execute("SELECT * FROM patients WHERE urgency = ? ORDER BY created_at DESC", (urgency_filter.upper(),))
    else:
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
        
    rows = cursor.fetchall()
    patients = [dict(row) for row in rows]
    conn.close()
    return patients

def get_patient_by_id(patient_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_stats() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM patients")
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as critical FROM patients WHERE urgency = 'CRITICAL'")
    critical = cursor.fetchone()["critical"]
    
    cursor.execute("SELECT COUNT(*) as medium FROM patients WHERE urgency = 'MEDIUM'")
    medium = cursor.fetchone()["medium"]
    
    cursor.execute("SELECT COUNT(*) as low FROM patients WHERE urgency = 'LOW'")
    low = cursor.fetchone()["low"]
    
    conn.close()
    return {
        "total": total,
        "critical": critical,
        "medium": medium,
        "low": low
    }
