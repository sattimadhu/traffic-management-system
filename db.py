import sqlite3

DATABASE = 'database/users.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    conn.commit()

    try:
        conn.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                     ('madhu', '2004', 1))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # admin already exists

    conn.close()

def get_user(username, password):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                        (username, password)).fetchone()
    conn.close()
    return user

def create_user(username, password):
    try:
        conn = get_connection()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
