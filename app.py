from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import gevent
from gevent import monkey
monkey.patch_all()
import os
from datetime import datetime
import json
import database as db
import sys
print("="*50)
print("🚀 APP.PY ЗАПУЩЕН!")
print(f"📁 Текущая папка: {os.getcwd()}")
print(f"📁 Файлы в папке: {os.listdir('.')}")
print("="*50)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'eptagram_secret_key_2024'
app.config['SECRET_KEY_TYPE'] = 'bytes'

socketio = SocketIO(app, 
                   cors_allowed_origins="*", 
                   async_mode='gevent',
                   ping_timeout=60,
                   ping_interval=25,
                   logger=False, 
                   engineio_logger=False)

user_sockets = {}
@app.route('/test')
def test_db():
    try:
        # Пробуем сохранить
        result = db.save_general_message('test_user', 'тестовое сообщение')
        if result:
            # Пробуем загрузить
            messages = db.get_general_messages(5)
            return f"""
            <h1>✅ ТЕСТ БД</h1>
            <p>Сообщение сохранено! ID: {result['id']}</p>
            <p>Всего сообщений: {len(messages)}</p>
            <p>Последнее: {messages[-1]['text'] if messages else 'нет'}</p>
            <pre>{messages}</pre>
            """
        else:
            return "<h1>❌ Ошибка сохранения</h1>"
    except Exception as e:
        return f"<h1>❌ Ошибка: {e}</h1>"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)