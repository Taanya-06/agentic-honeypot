import requests
from memory import get_session

GUVI_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_callback(session_id):
    session = get_session(session_id)

    final_intel = {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": [],
        "phoneNumbers": [],
        "suspiciousKeywords": []
    }

    for i in session["intel"]:
        for k in final_intel:
            final_intel[k].extend(i.get(k, []))

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(session["messages"]),
        "extractedIntelligence": final_intel,
        "agentNotes": "Urgency-based financial scam"
    }

    requests.post(GUVI_URL, json=payload, timeout=5)
