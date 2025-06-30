import sqlite3
from datetime import datetime

TRAFFIC_DB = 'database/traffic.db'

def get_connection():
    conn = sqlite3.connect(TRAFFIC_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_traffic_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Working', 'Not Working', 'Under Maintenance'))
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            description TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_signals():
    conn = get_connection()
    signals = conn.execute("SELECT * FROM signals").fetchall()
    conn.close()
    return signals

def add_signal(location, status):
    conn = get_connection()
    conn.execute("INSERT INTO signals (location, status) VALUES (?, ?)", (location, status))
    conn.commit()
    conn.close()

def delete_signal(signal_id):
    conn = get_connection()
    conn.execute("DELETE FROM signals WHERE id = ?", (signal_id,))
    conn.commit()
    conn.close()

def add_incident(location, incident_type, description):
    conn = get_connection()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('''
        INSERT INTO incidents (location, incident_type, description, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (location, incident_type, description, timestamp))
    conn.commit()
    conn.close()
def delete_incident(incident_id):
    conn = get_connection()
    conn.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()

def get_all_incidents():
    conn = get_connection()
    incidents = conn.execute("SELECT * FROM incidents ORDER BY timestamp DESC").fetchall()
    conn.close()
    return incidents

def get_all_signals():
    conn = get_connection()
    signals = conn.execute("SELECT * FROM signals").fetchall()
    conn.close()
    return signals
