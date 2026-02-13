import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
import hashlib

# База данных
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    """Создает все таблицы"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                avatar TEXT,
                bg_image TEXT,
                bg_pattern TEXT DEFAULT 'default',
                online INTEGER DEFAULT 0,
                last_seen TEXT,
                registered TEXT
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS general_messages (
                id SERIAL PRIMARY KEY,
                username TEXT,
                text TEXT,
                time TEXT,
                date TEXT
            )
        ''')
        
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
        print("✅ База данных инициализирована")
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")

# ============ ХЕЛПЕРЫ ============

def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(password, hash):
    """Проверка пароля"""
    return hash_password(password) == hash

# ============ ПОЛЬЗОВАТЕЛИ ============

def get_user_status(username):
    """Проверяет, существует ли пользователь"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT username FROM users WHERE username = %s', (username,))
        result = cur.fetchone()
        conn.close()
        
        if result:
            print(f"🔍 Пользователь {username} НАЙДЕН в БД")
            return True
        else:
            print(f"🔍 Пользователь {username} НЕ НАЙДЕН в БД")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки пользователя: {e}")
        return False

def add_user(username, password):
    """Добавляет нового пользователя с паролем"""
    try:
        conn = get_db()
        cur = conn.cursor()
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        password_hash = hash_password(password)
        
        cur.execute('SELECT username FROM users WHERE username = %s', (username,))
        if cur.fetchone():
            print(f"⚠️ Пользователь {username} УЖЕ существует")
            conn.close()
            return False
        
        cur.execute(
            'INSERT INTO users (username, password, registered, last_seen) VALUES (%s, %s, %s, %s)',
            (username, password_hash, now, now)
        )
        conn.commit()
        conn.close()
        print(f"✅ Пользователь {username} успешно добавлен")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка добавления пользователя: {e}")
        return False

def check_user(username, password):
    """Проверяет логин и пароль"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT password FROM users WHERE username = %s', (username,))
        result = cur.fetchone()
        conn.close()
        
        if result and validate_password(password, result['password']):
            print(f"✅ Успешный вход: {username}")
            return True
        print(f"❌ Неудачная попытка входа: {username}")
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки пользователя: {e}")
        return False

def update_avatar(username, avatar_base64):
    """Обновляет аватар пользователя"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE users SET avatar = %s WHERE username = %s', (avatar_base64, username))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка обновления аватара: {e}")
        return False

def get_avatar(username):
    """Получает аватар пользователя"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT avatar FROM users WHERE username = %s', (username,))
        result = cur.fetchone()
        conn.close()
        return result['avatar'] if result else None
    except Exception as e:
        print(f"❌ Ошибка получения аватара: {e}")
        return None

def update_bg_image(username, image_base64):
    """Обновляет фоновое изображение пользователя"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE users SET bg_image = %s WHERE username = %s', (image_base64, username))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка обновления фона: {e}")
        return False

def get_bg_image(username):
    """Получает фоновое изображение пользователя"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT bg_image FROM users WHERE username = %s', (username,))
        result = cur.fetchone()
        conn.close()
        return result['bg_image'] if result else None
    except Exception as e:
        print(f"❌ Ошибка получения фона: {e}")
        return None

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
        cur.execute('SELECT username, online, avatar FROM users ORDER BY username')
        rows = cur.fetchall()
        conn.close()
        return [{'username': row['username'], 'online': row['online'], 'avatar': row['avatar']} for row in rows]
    except Exception as e:
        print(f"❌ Ошибка загрузки пользователей: {e}")
        return []

# ============ ОБЩИЙ ЧАТ ============

def save_general_message(username, text):
    """Сохраняет сообщение в общий чат"""
    try:
        conn = get_db()
        cur = conn.cursor()
        now_time = datetime.now(timezone.utc).strftime('%H:%M')
        now_date = datetime.now(timezone.utc).strftime('%d.%m.%Y')
        
        print(f"💾 Сохраняю сообщение от {username}: {text[:30]}...")
        
        cur.execute(
            'INSERT INTO general_messages (username, text, time, date) VALUES (%s, %s, %s, %s) RETURNING id',
            (username, text, now_time, now_date)
        )
        message_id = cur.fetchone()['id']
        conn.commit()
        conn.close()
        
        print(f"✅ Сообщение СОХРАНЕНО! ID: {message_id}")
        
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

def get_general_messages(limit=50, offset=0):
    """Получает сообщения из общего чата"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT id, username, text, time, date FROM general_messages ORDER BY id DESC LIMIT %s OFFSET %s',
            (limit, offset)
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
        
        print(f"📖 Загружено {len(messages)} сообщений из БД")
        return messages
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return []

# ============ ЛИЧНЫЕ СООБЩЕНИЯ ============

def save_private_message(from_user, to_user, text):
    """Сохраняет личное сообщение"""
    try:
        conn = get_db()
        cur = conn.cursor()
        now_time = datetime.now(timezone.utc).strftime('%H:%M')
        now_date = datetime.now(timezone.utc).strftime('%d.%m.%Y')
        
        print(f"💾 Сохраняю личное: {from_user} -> {to_user}: {text[:30]}...")
        
        cur.execute(
            'INSERT INTO private_messages (from_user, to_user, text, time, date, is_read) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            (from_user, to_user, text, now_time, now_date, 0)
        )
        message_id = cur.fetchone()['id']
        conn.commit()
        conn.close()
        
        print(f"✅ Личное СОХРАНЕНО! ID: {message_id}")
        
        return {
            'id': message_id,
            'from': from_user,
            'to': to_user,
            'text': text,
            'time': now_time,
            'date': now_date
        }
    except Exception as e:
        print(f"❌ Ошибка сохранения личного: {e}")
        return None

def get_private_messages(user1, user2, limit=50, offset=0):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            '''SELECT id, from_user, to_user, text, time, date 
               FROM private_messages 
               WHERE (from_user = %s AND to_user = %s) OR (from_user = %s AND to_user = %s)
               ORDER BY id DESC LIMIT %s OFFSET %s''',
            (user1, user2, user2, user1, limit, offset)
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
        print(f"📖 Загружено {len(messages)} личных сообщений")
        return messages
    except Exception as e:
        print(f"❌ Ошибка загрузки личных: {e}")
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
