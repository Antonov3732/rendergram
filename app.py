# ============ ИМПОРТЫ ============
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import os
from datetime import datetime
import json
import database as db

# ============ ПРОВЕРКА RENDER ============
if os.environ.get('RENDER') or os.environ.get('DATABASE_URL'):
    os.environ['RENDER'] = 'true'

# ============ СОЗДАНИЕ ПРИЛОЖЕНИЯ ============
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'eptagram_secret_key_2024')
app.config['SECRET_KEY_TYPE'] = 'bytes'

# ============ НАСТРОЙКА SOCKETIO ============
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='gevent',
    ping_timeout=60,
    ping_interval=25,
    logger=False,
    engineio_logger=False
)

# ============ ХРАНИЛИЩЕ ============
user_sockets = {}

# ============ МАРШРУТЫ ============
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    if 'username' in session:
        return redirect(url_for('chat'))
    return render_template('register.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))

    all_users = db.get_all_users()
    current_avatar = db.get_avatar(session['username'])
    
    return render_template('chat.html',
                         username=session['username'],
                         users=all_users,
                         avatar=current_avatar)

# ============ АВТОРИЗАЦИЯ ============
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    
    if not username or not password:
        return 'Ник и пароль не могут быть пустыми'

    if db.check_user(username, password):
        session['username'] = username
        db.set_user_online(username, True)
        return redirect(url_for('chat'))
    else:
        return 'Неверный ник или пароль! <a href="/">Попробовать снова</a>'

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    confirm = request.form['confirm_password'].strip()
    
    if not username or not password:
        return 'Ник и пароль не могут быть пустыми'
    
    if password != confirm:
        return 'Пароли не совпадают! <a href="/register">Попробовать снова</a>'
    
    if len(password) < 4:
        return 'Пароль должен быть минимум 4 символа! <a href="/register">Попробовать снова</a>'

    if db.add_user(username, password):
        session['username'] = username
        db.set_user_online(username, True)
        return redirect(url_for('chat'))
    else:
        return 'Этот ник уже занят! <a href="/register">Попробовать другой</a>'

@app.route('/logout')
def logout():
    username = session.pop('username', None)
    if username:
        db.set_user_online(username, False)
        if username in user_sockets:
            del user_sockets[username]
        socketio.emit('user_offline', {'username': username}, broadcast=True)
    return redirect(url_for('index'))

# ============ API ДЛЯ АВАТАРОВ ============
@app.route('/api/avatar', methods=['POST'])
def update_avatar():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    avatar = data.get('avatar')
    
    if db.update_avatar(session['username'], avatar):
        # Оповещаем всех о новом аватаре
        socketio.emit('avatar_update', {
            'username': session['username'],
            'avatar': avatar
        }, broadcast=True)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Failed to update avatar'}), 400

@app.route('/api/avatar/<username>')
def get_avatar(username):
    avatar = db.get_avatar(username)
    return jsonify({'avatar': avatar})

# ============ API ДЛЯ СООБЩЕНИЙ ============
@app.route('/api/messages')
def get_messages():
    return jsonify(db.get_general_messages(50))

@app.route('/api/private/<string:user>')
def get_private_messages(user):
    current_user = session.get('username')
    if not current_user:
        return jsonify([])

    db.mark_private_as_read(user, current_user)
    messages = db.get_private_messages(current_user, user, 50)
    return jsonify(messages)

@app.route('/api/unread')
def get_unread():
    current_user = session.get('username')
    if not current_user:
        return jsonify({})
    return jsonify(db.get_unread_count(current_user))

# ============ SOCKET.IO СОБЫТИЯ ============
@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    if username:
        db.set_user_online(username, True)
        user_sockets[username] = request.sid
        all_users = db.get_all_users()
        emit('users_update', all_users, broadcast=True)
        print(f'{username} подключился')
    else:
        print('Анонимное подключение отклонено')
        return False

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username:
        db.set_user_online(username, False)
        if username in user_sockets:
            del user_sockets[username]
        emit('user_offline', {'username': username}, broadcast=True)
        print(f'{username} отключился')

@socketio.on('send_message')
def handle_message(data):
    username = session.get('username')
    if not username:
        return
    msg = db.save_general_message(username, data['text'])
    if msg:
        emit('new_message', msg, broadcast=True)

@socketio.on('send_private')
def handle_private(data):
    from_user = session.get('username')
    if not from_user:
        return
    to_user = data['to']
    text = data['text']

    msg = db.save_private_message(from_user, to_user, text)
    
    if msg:
        if to_user in user_sockets:
            emit('new_private', msg, room=user_sockets[to_user])
        emit('new_private', msg, room=request.sid)
        
        if to_user in user_sockets:
            unread = db.get_unread_count(to_user)
            emit('unread_update', unread, room=user_sockets[to_user])

@socketio.on('typing')
def handle_typing(data):
    username = session.get('username')
    if not username:
        return

    if data['to'] == 'general':
        emit('user_typing', {
            'username': username,
            'is_typing': data['is_typing']
        }, broadcast=True, include_self=False)
    else:
        if data['to'] in user_sockets:
            emit('user_typing_private', {
                'username': username,
                'is_typing': data['is_typing']
            }, room=user_sockets[data['to']])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
