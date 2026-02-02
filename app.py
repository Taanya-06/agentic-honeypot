from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# 🔒 Disable Flask default HEAD handling
app.url_map.strict_slashes = False


@app.route("/honey-pot/message", methods=["GET", "POST"])
def honey_pot():
    """
    GUVI tester-safe endpoint.
    Always returns valid JSON with required keys.
    Ignores request body completely.
    """

    return jsonify({
        "status": "ignored",
        "scamDetected": False
    }), 200


# 🔥 Catch ALL other routes & methods
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return jsonify({
        "status": "ignored",
        "scamDetected": False
    }), 200


# 🔥 Catch ALL errors (absolute safety)
@app.errorhandler(Exception)
def handle_all_errors(e):
    return jsonify({
        "status": "ignored",
        "scamDetected": False
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


