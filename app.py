from flask import Flask, request, render_template, send_from_directory
import json
import os

app = Flask(__name__)

STATUS_FILE = "status.json"

# Sikrer at status-filen findes
if not os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

#########################################
# LOGIN SIDE
#########################################

@app.route("/")
def login():
    return render_template("login.html")

#########################################
# STATUS SIDE
#########################################

@app.route("/status")
def status_page():
    return render_template("status.html")

#########################################
# API: Hent status.json
#########################################

@app.route("/get_status")
def get_status():
    if not os.path.exists(STATUS_FILE):
        return {"error": "status file missing"}, 404
    return send_from_directory(".", STATUS_FILE)

#########################################
# API: Upload status.json (fra lokalt script)
#########################################

API_KEY = "LP_TELEFON_84JH29XAQW"   # <<< du kan ændre denne

@app.route("/upload_status", methods=["POST"])
def upload_status():
    key = request.headers.get("X-API-KEY")

    if key != API_KEY:
        return {"error": "Unauthorized"}, 401

    data = request.json

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {"status": "OK"}, 200


#########################################
# RUN (ikke brugt på Render)
#########################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
