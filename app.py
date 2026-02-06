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
    try:
        # Always parse JSON safely
        data = request.get_json(force=True)

        text = data.get("message", {}).get("text", "")
        session_id = data.get("sessionId", "unknown")

        # Session memory (safe)
        init_session(session_id)
        add_message(session_id, text)

        # Scam logic
        if is_scam(text):
            reply = agent_reply(text)

            intel = extract(text)
            add_intel(session_id, intel)

            session = get_session(session_id)
            if session and not session.get("callbackSent"):
                try:
                    send_callback(session_id)
                    session["callbackSent"] = True
                except Exception:
                    pass
        else:
            reply = "Message received."

        # 🔴 SINGLE GUARANTEED RESPONSE FORMAT
        return jsonify({
            "status": "success",
            "reply": reply
        }), 200

    except Exception:
        # Even if EVERYTHING breaks, still return valid JSON
        return jsonify({
            "status": "success",
            "reply": "Message received."
        }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
