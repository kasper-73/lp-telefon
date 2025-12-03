from flask import Flask, render_template, request, redirect, session
import json, os

app = Flask(__name__)
app.secret_key = "LPSECRETKEY"

USERNAME="kasper"
PASSWORD="Bone2030"

# load status data if present
def load_status():
    if os.path.exists("status.json"):
        return json.load(open("status.json"))
    return {}

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form.get("username")==USERNAME and request.form.get("password")==PASSWORD:
            session["auth"]=True
            return redirect("/status")
        return render_template("login.html", error=True)
    return render_template("login.html")

@app.route("/status")
def status():
    if not session.get("auth"):
        return redirect("/")
    data = load_status()
    return render_template("status.html", data=data)

# endpoint to receive updates
@app.route("/update", methods=["POST"])
def update():
    token = request.headers.get("Authorization","")
    if token != "Bearer LP_TELEFON_84JH29XAQW":
        return {"error":"unauthorized"},401
    payload = request.json
    json.dump(payload, open("status.json","w"))
    return {"message":"ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
