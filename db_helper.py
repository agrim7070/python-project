import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash
DB_PATH = 'database.db'
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password_hash TEXT, is_admin INTEGER DEFAULT 0)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, glucose REAL, bloodpressure REAL, skinthickness REAL, insulin REAL, bmi REAL, pedigree REAL, age REAL, prediction INTEGER, probability REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        pwd = generate_password_hash('admin123')
        cur.execute("INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 1)", ('admin', pwd))
        conn.commit()
    conn.close()
def save_record(data: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''INSERT INTO patients (name, glucose, bloodpressure, skinthickness, insulin, bmi, pedigree, age, prediction, probability) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (data.get('name'), data.get('Glucose'), data.get('BloodPressure'), data.get('SkinThickness'), data.get('Insulin'), data.get('BMI'), data.get('DiabetesPedigreeFunction'), data.get('Age'), data.get('prediction'), data.get('probability')))
    conn.commit()
    conn.close()
def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, password_hash, is_admin FROM users WHERE username=?', (username,))
    row = cur.fetchone(); conn.close()
    if not row: return None
    uid, phash, is_admin = row
    if check_password_hash(phash, password): return {'id': uid, 'username': username, 'is_admin': bool(is_admin)}
    return None
def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        ph = generate_password_hash(password)
        cur.execute('INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 0)', (username, ph))
        conn.commit(); return True
    except Exception:
        return False
    finally:
        conn.close()
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*), SUM(prediction) FROM patients')
    total, positives = cur.fetchone()
    cur.execute("SELECT DATE(timestamp), COUNT(*) FROM patients GROUP BY DATE(timestamp) ORDER BY DATE(timestamp)")
    daily = cur.fetchall()
    conn.close(); return {'total': total or 0, 'positives': positives or 0, 'daily': daily}
