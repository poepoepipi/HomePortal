from flask import Flask, request, session, jsonify, redirect, render_template
import json
import os

app = Flask(__name__)
app.secret_key = "849242943849248hfjzhfkz39348hiezlu4294892"
PASSWORD = "temporary"
DATA_FILE = "data/bookmarks.json"


def load_bookmarks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_bookmarks(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def is_logged_in():
    return session.get("logged_in", False)


@app.route("/")
def boot():
    return render_template("boot.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/dashboard")
def home():
    if not is_logged_in():
        return redirect("/login")
    return render_template("dashboard.html")


@app.route("/bookmarks")
def bookmarks_page():
    if not is_logged_in():
        return redirect("/login")
    return render_template("bookmarks.html")


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
        "logged_in": is_logged_in()
    })


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})


@app.route("/api/bookmarks", methods=["GET"])
def get_bookmarks():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(load_bookmarks())


@app.route("/api/bookmarks", methods=["POST"])
def add_bookmark():
    if not is_logged_in():
        return jsonify({"error": "Unauthorized"}), 401

    data = load_bookmarks()
    new_item = request.get_json()

    if not new_item.get("title") or not new_item.get("url"):
        return jsonify({"error": "Missing title or url"}), 400

    data.append(new_item)
    save_bookmarks(data)

    return jsonify({"success": True})


@app.route("/api/bookmarks/<int:index>", methods=["DELETE"])
def delete_bookmark(index):
    if not is_logged_in():
        return jsonify({"error": "Unauthorized"}), 401

    data = load_bookmarks()

    if index < 0 or index >= len(data):
        return jsonify({"error": "Invalid index"}), 400

    data.pop(index)
    save_bookmarks(data)

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)