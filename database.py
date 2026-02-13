import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone

# Берем строку подключения из переменной окружения
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    """Подключение к PostgreSQL"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    """Создает таблицы при первом запуске"""
    conn = get_db()
    cur = conn.cursor()
    
    # Таблица пользователей
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            online INTEGER DEFAULT 0,
            last_seen TEXT,
            registered TEXT
        )
    ''')
    
    # Таблица общих сообщений
    cur.execute('''
        CREATE TABLE IF NOT EXISTS general_messages (
            id SERIAL PRIMARY KEY,
            username TEXT,
            text TEXT,
            time TEXT,
            date TEXT
        )
    ''')
    
    # Таблица личных сообщений
    cur.execute('''
        CREATE TABLE IF NOT EXISTS private_messages (
            id SERIAL PRIMARY KEY,
            from_user TEXT,
            to_user TEXT,
            text TEXT,
            time TEXT,
            date TEXT,
            is_read INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ PostgreSQL база данных инициализирована")

# ============ ПОЛЬЗОВАТЕЛИ ============

def add_user(username):
    try:
        conn = get_db()
        cur = conn.cursor()
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(
            'INSERT INTO users (username, registered, last_seen) VALUES (%s, %s, %s)',
            (username, now, now)
        )
        conn.commit()
        conn.close()
        print(f"👤 Пользователь {username} добавлен")
        return True
    except psycopg2.IntegrityError:
        print(f"⚠️ Пользователь {username} уже существует")
        return False
    except Exception as e:
        print(f"❌ Ошибка добавления пользователя: {e}")
        return False

def set_user_online(username, online=True):
    try:
        conn = get_db()
        cur = conn.cursor()
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(
            'UPDATE users SET online = %s, last_seen = %s WHERE username = %s',
            (1 if online else 0, now, username)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка обновления статуса: {e}")

def get_all_users():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT username, online FROM users ORDER BY username')
        rows = cur.fetchall()
        conn.close()
        users = [{'username': row['username'], 'online': row['online']} for row in rows]
        print(f"📋 Загружено {len(users)} пользователей")
        return users
    except Exception as e:
        print(f"❌ Ошибка загрузки пользователей: {e}")
        return []

def get_user_status(username):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT online FROM users WHERE username = %s', (username,))
        result = cur.fetchone()
        conn.close()
        return result['online'] if result else None
    except Exception as e:
        print(f"❌ Ошибка проверки статуса: {e}")
        return None

# ============ ОБЩИЙ ЧАТ ============

def save_general_message(username, text):
    try:
        conn = get_db()
        cur = conn.cursor()
        now_time = datetime.now(timezone.utc).strftime('%H:%M')
        now_date = datetime.now(timezone.utc).strftime('%d.%m.%Y')
        
        cur.execute(
            'INSERT INTO general_messages (username, text, time, date) VALUES (%s, %s, %s, %s) RETURNING id',
            (username, text, now_time, now_date)
        )
        message_id = cur.fetchone()['id']
        conn.commit()
        conn.close()
        
        print(f"✅ Сообщение сохранено! ID: {message_id}, от: {username}")
        
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
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT id, username, text, time, date FROM general_messages ORDER BY id DESC LIMIT %s',
            (limit,)
        )
        rows = cur.fetchall()
        conn.close()
        
        messages = []
        for row in reversed(rows):
            messages.append({
                'id': row['id'],
                'from': row['username'],
                'text': row['text'],
                'time': row['time'],
                'date': row['date']
            })
        print(f"📖 Загружено {len(messages)} сообщений из общего чата")
        return messages
    except Exception as e:
        print(f"❌ Ошибка загрузки сообщений: {e}")
        return []

# ============ ЛИЧНЫЕ СООБЩЕНИЯ ============

def save_private_message(from_user, to_user, text):
    try:
        conn = get_db()
        cur = conn.cursor()
        now_time = datetime.now(timezone.utc).strftime('%H:%M')
        now_date = datetime.now(timezone.utc).strftime('%d.%m.%Y')
        
        cur.execute(
            'INSERT INTO private_messages (from_user, to_user, text, time, date, is_read) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            (from_user, to_user, text, now_time, now_date, 0)
        )
        message_id = cur.fetchone()['id']
        conn.commit()
        conn.close()
        
        print(f"✅ Личное сообщение сохранено! ID: {message_id}, от: {from_user} -> {to_user}")
        
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
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            '''SELECT id, from_user, to_user, text, time, date 
               FROM private_messages 
               WHERE (from_user = %s AND to_user = %s) OR (from_user = %s AND to_user = %s)
               ORDER BY id DESC LIMIT %s''',
            (user1, user2, user2, user1, limit)
        )
        rows = cur.fetchall()
        conn.close()
        
        messages = []
        for row in reversed(rows):
            messages.append({
                'id': row['id'],
                'from': row['from_user'],
                'to': row['to_user'],
                'text': row['text'],
                'time': row['time'],
                'date': row['date']
            })
        return messages
    except Exception as e:
        print(f"❌ Ошибка загрузки личных сообщений: {e}")
        return []

def mark_private_as_read(from_user, to_user):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'UPDATE private_messages SET is_read = 1 WHERE from_user = %s AND to_user = %s',
            (from_user, to_user)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка отметки прочитанных: {e}")

def get_unread_count(username):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT from_user, COUNT(*) FROM private_messages WHERE to_user = %s AND is_read = 0 GROUP BY from_user',
            (username,)
        )
        rows = cur.fetchall()
        conn.close()
        return {row['from_user']: row['count'] for row in rows}
    except Exception as e:
        print(f"❌ Ошибка загрузки непрочитанных: {e}")
        return {}

# Инициализация
init_db()