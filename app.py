from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

from detector import is_scam
from agent import agent_reply
from extractor import extract
from memory import init_session, add_message, add_intel, get_session
from callback import send_callback

load_dotenv()
API_KEY = os.getenv("API_KEY", "honeypot@123")

app = Flask(__name__)

@app.route("/honey-pot/message", methods=["GET", "POST"])
def honey_pot():

    # 🔹 GET = Health check only (browser / render)
    if request.method == "GET":
        return jsonify({
            "status": "success",
            "reply": "what should i do now??"
        }), 200

    # 🔐 API KEY CHECK
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({
            "status": "success",
            "reply": "Unauthorized request"
        }), 200

    # 📦 SAFE JSON READ
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "status": "success",
            "reply": "Message processed"
        }), 200

    # 🔹 EXTRACT INPUT SAFELY
    session_id = data.get("sessionId", "unknown-session")
    message_obj = data.get("message", {})
    text = message_obj.get("text", "")

    if not text:
        return jsonify({
            "status": "success",
            "reply": "Message processed"
        }), 200

    # 🧠 SESSION MEMORY
    init_session(session_id)
    add_message(session_id, text)

    # 🛑 SCAM DETECTION
    if not is_scam(text):
        return jsonify({
            "status": "success",
            "reply": "Message processed"
        }), 200

    # 🤖 AGENT REPLY (BASED ON SCAM MESSAGE)
    reply = agent_reply(text)

    # 🕵️ INTEL EXTRACTION (internal)
    intel = extract(text)
    add_intel(session_id, intel)

    # 🚨 CALLBACK (once, silent)
    session = get_session(session_id)
    if session and not session.get("callbackSent"):
        try:
            send_callback(session_id)
            session["callbackSent"] = True
        except Exception:
            pass

    # ✅ FINAL RESPONSE (GUVI FORMAT)
    return jsonify({
        "status": "success",
        "reply": reply
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


