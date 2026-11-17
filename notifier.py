"""
Notification & Webhook Dispatcher for PulseGuard Health
Dispatches alerts to Discord, Slack, and simulates automated SMS/Email delivery.
"""

import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def dispatch_discord_alert(patient_id: str, assessment: Dict[str, Any], patient_data: Dict[str, Any]) -> bool:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url or not webhook_url.startswith("https://discord.com/api/webhooks"):
        return False
        
    urgency = assessment["urgency"]
    # Color mapping: Red for critical, Orange for medium, Green for low
    colors = {
        "CRITICAL": 0xFF0033,  # Vivid Red
        "MEDIUM": 0xFFA500,    # Orange
        "LOW": 0x2ECC71        # Green
    }
    
    embed = {
        "title": f"🚨 Patient Triage Alert: {urgency} Priority",
        "description": f"**Patient ID:** `{patient_id}`\n**Patient:** {patient_data['full_name']} ({patient_data['age']}yo, {patient_data['gender']})",
        "color": colors.get(urgency, 0x3498DB),
        "fields": [
            {"name": "Chief Complaint", "value": patient_data['chief_complaint'], "inline": True},
            {"name": "Assigned Department", "value": assessment['department'], "inline": True},
            {"name": "Urgency Score", "value": f"{assessment['urgency_score']}/100", "inline": True},
            {"name": "Clinical Rationale", "value": assessment['clinical_rationale'], "inline": False},
            {"name": "Physician Summary", "value": f"```{assessment['physician_summary']}```", "inline": False}
        ],
        "footer": {"text": "PulseGuard AI Triage System • Automated Dispatch"}
    }
    
    try:
        res = requests.post(webhook_url, json={"embeds": [embed]}, timeout=6)
        return res.status_code in [200, 204]
    except Exception as e:
        print(f"[Notifier] Discord dispatch error: {e}")
        return False

def dispatch_slack_alert(patient_id: str, assessment: Dict[str, Any], patient_data: Dict[str, Any]) -> bool:
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url or not webhook_url.startswith("https://hooks.slack.com"):
        return False
        
    urgency = assessment["urgency"]
    text = (
        f"*🚨 Triage Alert: {urgency} Priority*\n"
        f"*Patient:* {patient_data['full_name']} (ID: `{patient_id}`)\n"
        f"*Complaint:* {patient_data['chief_complaint']}\n"
        f"*Department:* {assessment['department']} (Risk Score: {assessment['urgency_score']}/100)\n"
        f"*Rationale:* {assessment['clinical_rationale']}"
    )
    
    try:
        res = requests.post(webhook_url, json={"text": text}, timeout=6)
        return res.status_code == 200
    except Exception as e:
        print(f"[Notifier] Slack dispatch error: {e}")
        return False

def dispatch_all(patient_id: str, assessment: Dict[str, Any], patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Coordinates multi-channel notification dispatch.
    """
    discord_sent = dispatch_discord_alert(patient_id, assessment, patient_data)
    slack_sent = dispatch_slack_alert(patient_id, assessment, patient_data)
    
    # Terminal Log for Demonstration & Verification
    border = "=" * 60
    print(f"\n{border}")
    print(f"[TRIAGE DISPATCH EVENT] - Patient ID: {patient_id}")
    print(f">> Priority: {assessment['urgency']} (Score: {assessment['urgency_score']}/100)")
    print(f">> Patient: {patient_data['full_name']} | Department: {assessment['department']}")
    print(f">> Complaint: {patient_data['chief_complaint']}")
    print(f">> Rationale: {assessment['clinical_rationale']}")
    print(f">> Patient Guidance Drafted: \"{assessment['patient_message'][:90]}...\"")
    if discord_sent:
        print("[OK] Discord Webhook Alert: DISPATCHED")
    if slack_sent:
        print("[OK] Slack Webhook Alert: DISPATCHED")
    print(f"{border}\n")
    
    return {
        "discord_sent": discord_sent,
        "slack_sent": slack_sent,
        "status": "DISPATCHED"
    }
