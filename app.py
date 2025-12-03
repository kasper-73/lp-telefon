from flask import Flask, render_template, send_from_directory, jsonify
import json
import os

app = Flask(__name__)

# Path til status.json i rodmappen
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(BASE_DIR, "status.json")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/status")
def status_page():
    return render_template("status.html")

@app.route("/status.json")
def status_json():
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
