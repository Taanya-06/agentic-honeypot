# memory.py

sessions = {}

def init_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "intel": [],
            "callbackSent": False   # 🔒 NEW: prevents duplicate callbacks
        }

def add_message(session_id, message):
    sessions[session_id]["messages"].append(message)

def add_intel(session_id, intel):
    sessions[session_id]["intel"].append(intel)

def get_session(session_id):
    return sessions.get(session_id)

