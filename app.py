import os
import sqlite3
from flask import Flask, jsonify, reques

app = Flask(__name_)
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    cursor.execute("DELETE FROM users")
    cursor.executemany(
        "INSERT INTO users (id, username, email, role) VALUES (?, ?, ?, ?)",
        [
            (1, "alice", "alice@example.com", "USER"),
            (2, "admin", "admin@example.com", "ADMIN"),
        ],
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status", "ok"})


@app.route("/user", methods=["GET"])
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Raw string-formatted SQL query for defensive security testing
    query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    users = [
        {"id": row[0], "username": row[1], "email": row[2], "role": row[3]}
        for row in rows
    ]
    return jsonify(users)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
