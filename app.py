from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

STATUS_FILE = "status.json"
PASSWORD = "LP_TELEFON_84JH29XAQW"  # Login adgangskode


# -------------------------------------------------
# LOGIN-SIDE (GET for visning, POST for login)
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("password", "")

        if pw == PASSWORD:
            return redirect("/status")
        else:
            return render_template("login.html", error="Forkert kode!")

    return render_template("login.html")


# -------------------------------------------------
# STATUS-SIDE (viser medarbejdernes telefonstatus)
# -------------------------------------------------
@app.route("/status")
def status_page():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    return render_template("status.html", users=data)


# -------------------------------------------------
# API-ENDPOINT TIL UPLOAD FRA DIT LOKALE PYTHON-SCRIPT
# -------------------------------------------------
@app.route("/upload_status", methods=["POST"])
def upload_status():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # Gem filen
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({"success": true}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------
# FLASK START (Render bruger Gunicorn – dette bruges kun lokalt)
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
