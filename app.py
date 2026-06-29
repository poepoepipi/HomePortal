from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def boot():
    return render_template("boot.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def home():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)