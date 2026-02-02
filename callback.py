# callback.py

import requests
from memory import get_session

GUVI_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_callback(session_id):
    session = get_session(session_id)

    # 🔒 Safety check
    if not session:
        print("Callback skipped: session not found")
        return

    final_intel = {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": [],
        "phoneNumbers": [],
        "suspiciousKeywords": []
    }

    # Combine all extracted intelligence
    for item in session["intel"]:
        for key in final_intel:
            final_intel[key].extend(item.get(key, []))

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(session["messages"]),
        "extractedIntelligence": final_intel,
        "agentNotes": "Urgency-based financial scam"
    }

    # 🚨 SAFE, NON-BLOCKING CALLBACK
    try:
        requests.post(GUVI_URL, json=payload, timeout=2)
        print("GUVI callback sent successfully")
    except Exception as e:
        # Do NOT crash the API
        print("GUVI callback failed (safe ignore):", e)

