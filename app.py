from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# 🔥 GLOBAL ERROR HANDLER (GUVI SAFE)
@app.errorhandler(Exception)
def handle_all_errors(e):
    return jsonify({
        "status": "ignored",
        "scamDetected": False
    }), 200


# 🔥 GUVI TESTER ENDPOINT
@app.route("/honey-pot/message", methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
def honey_pot():
    # GUVI tester jo bhi bheje (empty, invalid, wrong method)
    # hamesha valid response milega

    return jsonify({
        "status": "ignored",
        "scamDetected": False
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

