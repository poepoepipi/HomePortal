from flask import Flask, request, session, jsonify, redirect, render_template

app = Flask(__name__)
app.secret_key = "849242943849248hfjzhfkz39348hiezlu4294892"
PASSWORD = "temporary"

@app.route("/")
def boot():
    return render_template("boot.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def home():
    return render_template("dashboard.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    password = data.get("password")

    if password == PASSWORD:
        session["logged_in"] = True
        return jsonify({"success": True})

    return jsonify({"success": False}), 401

@app.route("/api/session")
def check_session():
    return jsonify({
        "logged_in": session.get("logged_in", False)
    })

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)