import requests
from memory import get_session

GUVI_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_callback(session_id):
    session = get_session(session_id)
    if not session:
        return

    final_intel = {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": [],
        "phoneNumbers": [],
        "suspiciousKeywords": []
    }

    for intel in session["intel"]:
        for key in final_intel:
            final_intel[key].extend(intel.get(key, []))

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(session["messages"]),
        "extractedIntelligence": final_intel,
        "agentNotes": "Urgency-based financial scam"
    }

    try:
        requests.post(GUVI_URL, json=payload, timeout=5)
    except Exception:
        pass

