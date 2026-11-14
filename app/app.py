import sqlite3

from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)
    db = sqlite3.connect(":memory:", check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.executescript("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL)")
    db.executemany("INSERT INTO users (name, email) VALUES (?, ?)",
                   [("Aigerim", "aigerim@example.kz"), ("Dana", "dana@example.kz")])

    @app.get("/users")
    def list_users():
        rows = db.execute("SELECT id, name, email FROM users WHERE id > ?", (0,)).fetchall()
        return jsonify([dict(r) for r in rows])

    @app.get("/users/<int:user_id>")
    def get_user(user_id):
        row = db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
        return (jsonify(dict(row)), 200) if row else (jsonify({"error": "not found"}), 404)

    return app
