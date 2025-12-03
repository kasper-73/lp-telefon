from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

STATUS_FILE = "status.json"

# ------------------------------
# Forside – login eller redirect
# ------------------------------
@app.route("/")
def home():
    return render_template("login.html")

# ------------------------------
# Statusside (webvisning)
# ------------------------------
@app.route("/status")
def status_page():
    # Læs status fra JSON-filen hvis den findes
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    return render_template("status.html", users=data)

# ------------------------------
# API-endpoint til upload fra lokalt Python-script
# ------------------------------
@app.route("/upload_status", methods=["POST"])
def upload_status():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # Gem JSON i filen
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------
# Flask starter ikke i debug i Render (gunicorn bruges)
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
