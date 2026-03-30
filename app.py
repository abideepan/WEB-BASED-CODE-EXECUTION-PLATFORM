from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector

app = Flask(__name__)

# =========================
# 🔌 MySQL Connection
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="P@$$w0rd",   # 🔴 change this
    database="compiler_db"
)
cursor = db.cursor()

# =========================
# 🌐 Pages
# =========================
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/compiler")
def compiler():
    return render_template("index.html")

@app.route("/register_page")
def register_page():
    return render_template("register.html")

# =========================
# 🔐 Register
# =========================
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (data["username"], data["password"])
    )
    db.commit()

    return jsonify({"message": "Registered successfully"})

# =========================
# 🔓 Login
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (data["username"], data["password"])
    )
    user = cursor.fetchone()

    if user:
        return jsonify({
            "message": "Login success",
            "user_id": user[0]
        })
    else:
        return jsonify({
            "message": "Invalid credentials"
        })

# =========================
# ▶️ Run Code (FREE Judge0)
# =========================
@app.route("/run", methods=["POST"])
def run_code():
    data = request.json

    payload = {
        "source_code": data["code"],
        "language_id": int(data["language"]),
        "stdin": data.get("input", "")
    }

    try:
        # FREE Judge0 API (no key needed)
        response = requests.post(
            "https://ce.judge0.com/submissions?base64_encoded=false&wait=true",
            json=payload
        )

        result = response.json()

        # Extract clean output
        clean_output = (
                result.get("stdout") or
                result.get("stderr") or
                result.get("compile_output") or
                "No output"
        )

        # Save only clean output
        if data.get("user_id"):
            cursor.execute(
                "INSERT INTO history (user_id, code, language, output) VALUES (%s,%s,%s,%s)",
                (data["user_id"], data["code"], data["language"], clean_output)
            )
            db.commit()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================
# 📜 History
# =========================
@app.route("/history/<int:user_id>")
def history(user_id):
    cursor.execute(
        "SELECT code, language, output FROM history WHERE user_id=%s",
        (user_id,)
    )
    data = cursor.fetchall()

    return jsonify(data)

# =========================
# ▶️ Run Server
# =========================
if __name__ == "__main__":
    app.run(debug=True)