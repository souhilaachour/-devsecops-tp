from flask import Flask, request, abort
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'test.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (1, 'admin', 'admin123'))
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (2, 'user', 'password'))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "Hello from DevSecOps demo app!"

@app.route('/login')
def login():
    username = request.args.get('username', '').strip()
    password = request.args.get('password', '').strip()
    if not username or not password:
        abort(400, description="Bad Request: username and password required")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Requête paramétrée pour éviter l'injection SQL
    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return f"Login successful for user: {user[1]}"
    else:
        abort(401, description="Unauthorized: invalid credentials")

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
