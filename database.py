import sqlite3
from datetime import datetime, timezone
import os

# Определяем путь к БД
if os.environ.get('RENDER'):
    DB_PATH = '/tmp/eptagram.db'
    print(f"🎯 Render режим: БД в /tmp/")
else:
    DB_PATH = 'eptagram.db'
    print(f"💻 Локальный режим: БД в текущей папке")

print(f"📁 База данных: {DB_PATH}")

def init_db():
    """Создает таблицы при первом запуске"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY,
                      online INTEGER DEFAULT 0,
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
                      is_read INTEGER DEFAULT 0)''')
        
        conn.commit()
        conn.close()
        print("✅ База данных инициализирована")
        return True
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")
        return False

# ============ ПОЛЬЗОВАТЕЛИ ============

def add_user(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO users (username, registered, last_seen) VALUES (?, ?, ?)',
                 (username, now, now))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"❌ Ошибка добавления пользователя: {e}")
        return False

def set_user_online(username, online=True):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        c.execute('UPDATE users SET online = ?, last_seen = ? WHERE username = ?',
                 (1 if online else 0, now, username))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка обновления статуса: {e}")

def get_all_users():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT username, online FROM users ORDER BY username')
        rows = c.fetchall()
        conn.close()
        return [{'username': row[0], 'online': bool(row[1])} for row in rows]
    except Exception as e:
        print(f"❌ Ошибка загрузки пользователей: {e}")
        return []

def get_user_status(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT online FROM users WHERE username = ?', (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"❌ Ошибка проверки статуса: {e}")
        return None

# ============ ОБЩИЙ ЧАТ ============

def save_general_message(username, text):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        now_time = datetime.now(timezone.utc).strftime('%H:%M')
        now_date = datetime.now(timezone.utc).strftime('%d.%m.%Y')
        
        c.execute('''INSERT INTO general_messages (username, text, time, date)
                     VALUES (?, ?, ?, ?)''', (username, text, now_time, now_date))
        message_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': message_id,
            'from': username,
            'text': text,
            'time': now_time,
            'date': now_date
        }
    except Exception as e:
        print(f"❌ Ошибка сохранения сообщения: {e}")
        return None

def get_general_messages(limit=50):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT id, username, text, time, date 
                     FROM general_messages 
                     ORDER BY id DESC LIMIT ?''', (limit,))
        rows = c.fetchall()
        conn.close()
        
        messages = []
        for row in reversed(rows):
            messages.append({
                'id': row[0],
                'from': row[1],
                'text': row[2],
                'time': row[3],
                'date': row[4]
            })
        return messages
    except Exception as e:
        print(f"❌ Ошибка загрузки сообщений: {e}")
        return []

# ============ ЛИЧНЫЕ СООБЩЕНИЯ ============

def save_private_message(from_user, to_user, text):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        now_time = datetime.now(timezone.utc).strftime('%H:%M')
        now_date = datetime.now(timezone.utc).strftime('%d.%m.%Y')
        
        c.execute('''INSERT INTO private_messages (from_user, to_user, text, time, date, is_read)
                     VALUES (?, ?, ?, ?, ?, 0)''', (from_user, to_user, text, now_time, now_date))
        message_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'id': message_id,
            'from': from_user,
            'to': to_user,
            'text': text,
            'time': now_time,
            'date': now_date
        }
    except Exception as e:
        print(f"❌ Ошибка сохранения личного сообщения: {e}")
        return None

def get_private_messages(user1, user2, limit=50):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT id, from_user, to_user, text, time, date 
                     FROM private_messages 
                     WHERE (from_user = ? AND to_user = ?) OR (from_user = ? AND to_user = ?)
                     ORDER BY id DESC LIMIT ?''', (user1, user2, user2, user1, limit))
        rows = c.fetchall()
        conn.close()
        
        messages = []
        for row in reversed(rows):
            messages.append({
                'id': row[0],
                'from': row[1],
                'to': row[2],
                'text': row[3],
                'time': row[4],
                'date': row[5]
            })
        return messages
    except Exception as e:
        print(f"❌ Ошибка загрузки личных сообщений: {e}")
        return []

def mark_private_as_read(from_user, to_user):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''UPDATE private_messages 
                     SET is_read = 1 
                     WHERE from_user = ? AND to_user = ?''', (from_user, to_user))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка отметки прочитанных: {e}")

def get_unread_count(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT from_user, COUNT(*) 
                     FROM private_messages 
                     WHERE to_user = ? AND is_read = 0
                     GROUP BY from_user''', (username,))
        rows = c.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}
    except Exception as e:
        print(f"❌ Ошибка загрузки непрочитанных: {e}")
        return {}

# Инициализация
init_db()