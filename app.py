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

@app.route("/honey-pot/message", methods=["POST"])
def honey_pot():

    # 🔐 API KEY CHECK
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # 📦 JSON READ
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    session_id = data.get("sessionId")
    message_obj = data.get("message", {})
    text = message_obj.get("text")

    if not session_id or not text:
        return jsonify({"error": "Invalid payload"}), 400

    # 🧠 SESSION
    init_session(session_id)
    add_message(session_id, text)

    # 🛑 SCAM CHECK
    if not is_scam(text):
        return jsonify({
            "status": "ignored",
            "scamDetected": False
        }), 200

    # 🤖 AGENT RESPONSE (✅ FIXED)
    reply = agent_reply(text)

    # 🕵️ EXTRACT INTEL
    intel = extract(text)
    add_intel(session_id, intel)

    # 🚨 CALLBACK ONCE
    session = get_session(session_id)
    if session and not session.get("callbackSent"):
        send_callback(session_id)
        session["callbackSent"] = True

    return jsonify({
        "status": "success",
        "scamDetected": True,
        "reply": reply
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
