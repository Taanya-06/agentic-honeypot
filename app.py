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

# ✅ GET + POST dono allow (GUVI tester ke liye)
@app.route("/honey-pot/message", methods=["GET", "POST"])
def honey_pot():

    # 🔐 API KEY CHECK (GUVI tester bhi bhejta hai)
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # 🧪 GUVI TESTER – GET REQUEST
    if request.method == "GET":
        return jsonify({
            "status": "ok",
            "message": "Honeypot API reachable and authenticated"
        }), 200

    # 🧪 GUVI TESTER – POST WITHOUT JSON / EMPTY BODY
    if not request.is_json:
        return jsonify({
            "status": "ok",
            "message": "Honeypot API reachable and authenticated"
        }), 200

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "ok",
            "message": "Honeypot API reachable and authenticated"
        }), 200

    # 🧾 REQUIRED FIELD CHECKS (REAL REQUESTS ONLY)
    if "sessionId" not in data:
        return jsonify({"error": "Missing sessionId"}), 400

    if "message" not in data or "text" not in data["message"]:
        return jsonify({"error": "Invalid message format"}), 400

    session_id = data["sessionId"]
    message = data["message"]["text"]

    # 🧠 SESSION INIT
    init_session(session_id)
    add_message(session_id, message)

    # 🛑 SCAM DETECTION
    if not is_scam(message):
        return jsonify({
            "status": "ignored",
            "scamDetected": False
        })

    # 🤖 AGENT RESPONSE
    reply = agent_reply()

    # 🕵️ INTELLIGENCE EXTRACTION
    intel = extract(message)
    add_intel(session_id, intel)

    # 🚨 FINAL CALLBACK (ONLY ONCE PER SESSION)
    session = get_session(session_id)
    if (
        session
        and not session.get("callbackSent")
        and (intel.get("upiIds") or intel.get("phishingLinks") or intel.get("bankAccounts"))
    ):
        send_callback(session_id)
        session["callbackSent"] = True

    return jsonify({
        "status": "success",
        "scamDetected": True,
        "reply": reply
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

