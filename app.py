from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import gevent
from gevent import monkey
import os
from datetime import datetime
import json
import database as db

monkey.patch_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eptagram_secret_key_2024'
app.config['SECRET_KEY_TYPE'] = 'bytes'  
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_timeout=60,ping_interval=25, logger=False, engineio_logger=False)

# Хранилище socket.id
user_sockets = {}

# ============ СТРАНИЦЫ ============

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat'))
    return render_template('login.html') # ← ИЗМЕНИЛ НА login.html!

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))

    all_users = db.get_all_users()
    other_users = [u['username'] for u in all_users if u['username'] != session['username']]

    return render_template('chat.html', # ← ТЕПЕРЬ chat.html
                         username=session['username'],
                         users=other_users)

# ============ АВТОРИЗАЦИЯ ============

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip()
    if not username:
        return 'Ник не может быть пустым'

    if db.get_user_status(username) is not None:
        return 'Этот ник уже занят! <a href="/">Попробовать другой</a>'

    db.add_user(username)
    session['username'] = username
    db.set_user_online(username, True)

    return redirect(url_for('chat'))

@app.route('/logout')
def logout():
    username = session.pop('username', None)
    if username:
        db.set_user_online(username, False)
        if username in user_sockets:
            del user_sockets[username]
        socketio.emit('user_offline', {'username': username}, broadcast=True)
    return redirect(url_for('index'))

# ============ API ============

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

# ============ SOCKET.IO ============

@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    if username:
        db.set_user_online(username, True)
        user_sockets[username] = request.sid
        all_users = db.get_all_users()
        emit('users_update', all_users, broadcast=True)
        print(f'{username} подключился')

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
    username = session['username']
    msg = db.save_general_message(username, data['text'])
    emit('new_message', msg, broadcast=True)

@socketio.on('send_private')
def handle_private(data):
    from_user = session['username']
    to_user = data['to']
    text = data['text']

    msg = db.save_private_message(from_user, to_user, text)

    if to_user in user_sockets:
        emit('new_private', msg, room=user_sockets[to_user])

    emit('new_private', msg, room=request.sid)

    if to_user in user_sockets:
        unread = db.get_unread_count(to_user)
        emit('unread_update', unread, room=user_sockets[to_user])

@socketio.on('typing')
def handle_typing(data):
    username = session['username']

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

# Закомментировано для PythonAnywhere
if __name__ == '__main__':
 port = int(os.environ.get('PORT', 5000))
 socketio.run(app, host='0.0.0.0', port=port, debug=True)
