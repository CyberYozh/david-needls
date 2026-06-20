# sudo apt update
# sudo apt install python3-venv
# python3 -m venv env
# source env/bin/active
# pip install flask pyjwt

from flask import Flask, request, jsonify
import sqlite3
import jwt
import datetime
import os
import subprocess

app = Flask(__name__)

SECRET_KEY = "password123"


def init_db():
    conn = sqlite3.connect("ctf.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("DELETE FROM users")

    cur.execute("""
    INSERT INTO users(username,password)
    VALUES
    ('admin','SuperSecretPassword'),
    ('alice','alice123'),
    ('bob','bob123')
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return jsonify({
        "message": "Flask CTF API",
        "endpoints": [
            "/login",
            "/user?id=1",
            "/file?name=test.txt",
            "/ping?host=127.0.0.1",
            "/search?username=admin"
        ]
    })



@app.route("/login", methods=["POST"])
def login():

    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("ctf.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()

    if not user:
        return jsonify({"error": "invalid credentials"}), 401

    token = jwt.encode(
        {
            "id": user[0],
            "username": user[1],
            "role": "user",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token})



@app.route("/user")
def user():

    user_id = request.args.get("id")

    conn = sqlite3.connect("ctf.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT id,username,password FROM users WHERE id=?",
        (user_id,)
    )

    user = cur.fetchone()

    if not user:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "id": user[0],
        "username": user[1],
        "password": user[2]
    })



@app.route("/search")
def search():

    username = request.args.get("username", "")

    conn = sqlite3.connect("ctf.db")
    cur = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}'"

    result = cur.execute(query).fetchall()

    return jsonify({
        "query": query,
        "result": result
    })



@app.route("/file")
def file():

    filename = request.args.get("name")

    with open(filename, "r") as f:
        return f.read()



@app.route("/ping")
def ping():

    host = request.args.get("host")

    command = f"ping -c 1 {host}"

    output = subprocess.getoutput(command)

    return jsonify({
        "command": command,
        "output": output
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
