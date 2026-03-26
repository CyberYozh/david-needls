# Прежде всего, сделайте следующее:
# Создайте папку:
# mkdir api
# вставьте этот код в файл app.py
# создайте виртуальное окружение:
# python3 -m venv env
# активируйте его:
# source env/bin/activate
# установите Flask:
# pip3 install flask
# запустите приложение:
# python3 app.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake database
users = [
    {"id": 1, "username": "admin", "password": "admin123", "role": "admin"},
    {"id": 2, "username": "john", "password": "john123", "role": "user"},
    {"id": 3, "username": "alice", "password": "alice123", "role": "user"},
]

# ---------------------------
# 1. Login (NO RATE LIMITING)
# ---------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and user["password"] == password:
            return jsonify({
                "message": "Login successful",
                "user_id": user["id"],
                "role": user["role"]
            })

    return jsonify({"message": "Invalid credentials"}), 401


# -----------------------------------
# 2. Get User (IDOR VULNERABILITY)
# -----------------------------------
@app.route('/user', methods=['GET'])
def get_user():
    user_id = int(request.args.get("id"))

    for user in users:
        if user["id"] == user_id:
            return jsonify(user)  # ❌ exposes password + no auth check

    return jsonify({"message": "User not found"}), 404


# -----------------------------------
# 3. Admin Panel (BROKEN AUTH)
# -----------------------------------
@app.route('/admin', methods=['GET'])
def admin():
    role = request.headers.get("role")  # ❌ trusting user input

    if role == "admin":
        return jsonify({
            "message": "Welcome admin",
            "all_users": users
        })

    return jsonify({"message": "Access denied"}), 403


# -----------------------------------
# 4. Update Password (NO AUTH)
# -----------------------------------
@app.route('/update_password', methods=['POST'])
def update_password():
    data = request.json
    user_id = data.get("id")
    new_password = data.get("new_password")

    for user in users:
        if user["id"] == user_id:
            user["password"] = new_password
            return jsonify({"message": "Password updated"})

    return jsonify({"message": "User not found"}), 404


# -----------------------------------
# 5. Debug Endpoint (DATA LEAK)
# -----------------------------------
@app.route('/debug', methods=['GET'])
def debug():
    return jsonify({
        "server": "dev",
        "database": "users_db",
        "users": users  # ❌ massive data exposure
    })


if __name__ == '__main__':
    app.run(debug=True)
