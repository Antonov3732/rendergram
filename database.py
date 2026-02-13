import sqlite3
from datetime import datetime, timezone
import os

# ✅ ФИНАЛЬНОЕ РЕШЕНИЕ ДЛЯ RENDER
if os.environ.get('RENDER'):
    # Используем persistent disk
    DB_PATH = '/opt/render/project/data/eptagram.db'
    # Создаем папку если её нет
    os.makedirs('/opt/render/project/data', exist_ok=True)
else:
    DB_PATH = 'eptagram.db'

print(f"🔥 БАЗА ДАННЫХ: {DB_PATH}")
print(f"📁 Папка существует? {os.path.exists(os.path.dirname(DB_PATH))}")

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
        print(f"💾 Файл БД: {DB_PATH}")
        print(f"📁 Файл существует? {os.path.exists(DB_PATH)}")
        return True
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")
        return False

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
        
        print(f"✅ СОХРАНЕНО! ID: {message_id}, Текст: {text[:20]}")
        print(f"💾 БД: {DB_PATH}, размер: {os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0} байт")
        
        return {
            'id': message_id,
            'from': username,
            'text': text,
            'time': now_time,
            'date': now_date
        }
    except Exception as e:
        print(f"❌ ОШИБКА СОХРАНЕНИЯ: {e}")
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
        print(f"📖 ЗАГРУЖЕНО {len(messages)} сообщений")
        return messages
    except Exception as e:
        print(f"❌ ОШИБКА ЗАГРУЗКИ: {e}")
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
        
        print(f"✅ ЛИЧНОЕ СОХРАНЕНО! ID: {message_id}")
        
        return {
            'id': message_id,
            'from': from_user,
            'to': to_user,
            'text': text,
            'time': now_time,
            'date': now_date
        }
    except Exception as e:
        print(f"❌ ОШИБКА СОХРАНЕНИЯ ЛИЧНОГО: {e}")
        return None

# ... остальные функции без изменений ...

init_db()