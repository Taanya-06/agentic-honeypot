from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

from detector import is_scam
from agent import agent_reply
from extractor import extract
from memory import init_session, add_message, add_intel, get_session
from callback import send_callback

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

# 🔹 GUVI TESTER / HEALTH CHECK
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# 🔹 REAL AI HONEYPOT (PDF COMPLIANT)
@app.route("/honey-pot/message", methods=["POST"])
def honey_pot():

    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    session_id = data.get("sessionId")
    message_obj = data.get("message", {})
    text = message_obj.get("text")

    if not session_id or not text:
        return jsonify({"error": "Invalid payload"}), 400

    init_session(session_id)
    add_message(session_id, text)

    if not is_scam(text):
        return jsonify({
            "status": "ignored",
            "scamDetected": False
        }), 200

    reply = agent_reply()
    intel = extract(text)
    add_intel(session_id, intel)

    session = get_session(session_id)
    if not session.get("callbackSent"):
        send_callback(session_id)
        session["callbackSent"] = True

    return jsonify({
        "status": "success",
        "reply": reply
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

