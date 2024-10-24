import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

def signup_user(username, password, role):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def user_exists(username):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user
