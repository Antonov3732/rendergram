import sqlite3
from datetime import datetime
import pytz
import os

DB_PATH = 'eptagram.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  online BOOLEAN DEFAULT 0,
                  last_seen TEXT,
                  registered TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS general_messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  text TEXT,
                  time TEXT,
                  date TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS private_messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  from_user TEXT,
                  to_user TEXT,
                  text TEXT,
                  time TEXT,
                  date TEXT,
                  is_read BOOLEAN DEFAULT 0)''')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

# ============ ПОЛЬЗОВАТЕЛИ ============

def add_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    try:
        c.execute('INSERT INTO users (username, registered, last_seen) VALUES (?, ?, ?)',
                 (username, now, now))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def remove_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

def set_user_online(username, online=True):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    c.execute('UPDATE users SET online = ?, last_seen = ? WHERE username = ?',
             (1 if online else 0, now, username))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT username, online FROM users ORDER BY username')
    users = [{'username': row[0], 'online': bool(row[1])} for row in c.fetchall()]
    conn.close()
    return users

def get_user_status(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT online FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# ============ ОБЩИЙ ЧАТ ============

def save_general_message(username, text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now_utc = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    now_date = datetime.now(pytz.UTC).strftime('%d.%m.%Y')
    c.execute('''INSERT INTO general_messages (username, text, time, date)
                 VALUES (?, ?, ?, ?)''', (username, text, now_utc, now_date))
    message_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        'id': message_id,
        'from': username,
        'text': text,
        'time': now_utc,
        'date': now_date
    }

def get_general_messages(limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, username, text, time, date 
                 FROM general_messages 
                 ORDER BY id DESC LIMIT ?''', (limit,))
    messages = []
    for row in reversed(list(c.fetchall())):
        messages.append({
            'id': row[0],
            'from': row[1],
            'text': row[2],
            'time': row[3],
            'date': row[4]
        })
    conn.close()
    return messages

# ============ ЛИЧНЫЕ СООБЩЕНИЯ ============

def save_private_message(from_user, to_user, text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now_utc = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    now_date = datetime.now(pytz.UTC).strftime('%d.%m.%Y')
    c.execute('''INSERT INTO private_messages (from_user, to_user, text, time, date, is_read)
                 VALUES (?, ?, ?, ?, ?, 0)''', (from_user, to_user, text, now_utc, now_date))
    message_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        'id': message_id,
        'from': from_user,
        'to': to_user,
        'text': text,
        'time': now_utc,
        'date': now_date
    }

def get_private_messages(user1, user2, limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, from_user, to_user, text, time, date 
                 FROM private_messages 
                 WHERE (from_user = ? AND to_user = ?) OR (from_user = ? AND to_user = ?)
                 ORDER BY id DESC LIMIT ?''', (user1, user2, user2, user1, limit))
    messages = []
    for row in reversed(list(c.fetchall())):
        messages.append({
            'id': row[0],
            'from': row[1],
            'to': row[2],
            'text': row[3],
            'time': row[4],
            'date': row[5]
        })
    conn.close()
    return messages

def mark_private_as_read(from_user, to_user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''UPDATE private_messages 
                 SET is_read = 1 
                 WHERE from_user = ? AND to_user = ?''', (from_user, to_user))
    conn.commit()
    conn.close()

def get_unread_count(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT from_user, COUNT(*) 
                 FROM private_messages 
                 WHERE to_user = ? AND is_read = 0
                 GROUP BY from_user''', (username,))
    result = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return result

init_db()