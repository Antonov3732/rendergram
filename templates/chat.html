<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>EptaGram</title>
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        body {
            background: #000;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .app {
            width: 100%;
            height: 100vh;
            display: flex;
            background: #0a0a0a;
            position: relative;
        }
        
        .sidebar {
            width: 280px;
            background: #0a0a0a;
            border-right: 1px solid #1a1a1a;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s ease;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                position: absolute;
                top: 0;
                left: 0;
                bottom: 0;
                width: 85%;
                max-width: 320px;
                background: #0a0a0a;
                z-index: 100;
                transform: translateX(-100%);
                box-shadow: 2px 0 20px rgba(0,0,0,0.5);
            }
            
            .sidebar.open {
                transform: translateX(0);
            }
            
            .overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.7);
                z-index: 90;
                display: none;
            }
            
            .overlay.show {
                display: block;
            }
            
            .menu-toggle {
                display: block !important;
            }
        }
        
        .menu-toggle {
            display: none;
            position: fixed;
            top: 16px;
            left: 16px;
            z-index: 200;
            background: #1a1a1a;
            border: none;
            color: #fff;
            font-size: 24px;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
        }
        
        .user {
            padding: 20px;
            border-bottom: 1px solid #1a1a1a;
        }
        
        .user-name {
            color: #fff;
            font-weight: 600;
            font-size: clamp(16px, 4vw, 18px);
            margin-bottom: 8px;
        }
        
        .logout {
            color: #888;
            text-decoration: none;
            font-size: clamp(12px, 3vw, 13px);
        }
        
        .channels {
            flex: 1;
            overflow-y: auto;
            padding: clamp(12px, 3vw, 16px);
        }
        
        .channel {
            padding: clamp(10px, 2.5vw, 12px) clamp(12px, 3vw, 16px);
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 4px;
            color: #ccc;
            display: flex;
            align-items: center;
            transition: 0.2s;
            font-size: clamp(13px, 3.5vw, 14px);
        }
        
        .channel:hover {
            background: #1a1a1a;
        }
        
        .channel.active {
            background: #2d2d2d;
            color: #fff;
        }
        
        .online-status {
            width: clamp(6px, 2vw, 8px);
            height: clamp(6px, 2vw, 8px);
            border-radius: 50%;
            margin-right: 10px;
            flex-shrink: 0;
        }
        
        .online { background: #00ff88; }
        .offline { background: #666; }
        
        .divider {
            color: #666;
            font-size: clamp(10px, 2.5vw, 11px);
            padding: 16px 16px 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .badge {
            background: #ff4444;
            color: white;
            border-radius: 12px;
            padding: 2px 8px;
            font-size: clamp(10px, 2.5vw, 11px);
            margin-left: auto;
            flex-shrink: 0;
        }
        
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #0a0a0a;
            width: 100%;
        }
        
        .header {
            padding: clamp(16px, 4vw, 20px);
            border-bottom: 1px solid #1a1a1a;
            color: #fff;
            font-weight: 500;
            font-size: clamp(16px, 4vw, 18px);
            margin-left: clamp(0px, 10vw, 0px);
        }
        
        @media (max-width: 768px) {
            .header {
                margin-left: 60px;
            }
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: clamp(16px, 4vw, 24px);
            display: flex;
            flex-direction: column;
            gap: clamp(12px, 3vw, 16px);
        }
        
        .message {
            max-width: min(70%, 600px);
            display: flex;
            flex-direction: column;
        }
        
        .message.own {
            align-self: flex-end;
        }
        
        .message-sender {
            font-size: clamp(11px, 2.8vw, 12px);
            color: #888;
            margin-bottom: 4px;
            padding-left: 4px;
        }
        
        .message-bubble {
            padding: clamp(8px, 2.5vw, 12px) clamp(12px, 3vw, 16px);
            background: #1a1a1a;
            border-radius: 18px;
            color: #fff;
            word-break: break-word;
            font-size: clamp(13px, 3.5vw, 14px);
            line-height: 1.4;
        }
        
        .message.own .message-bubble {
            background: #2d2d2d;
        }
        
        .message-time {
            font-size: clamp(9px, 2.2vw, 10px);
            color: #666;
            margin-top: 4px;
            align-self: flex-end;
            padding-right: 4px;
        }
        
        .input-area {
            padding: clamp(12px, 3vw, 16px) clamp(16px, 4vw, 20px);
            border-top: 1px solid #1a1a1a;
            display: flex;
            gap: clamp(8px, 2vw, 12px);
            background: #0a0a0a;
        }
        
        .input-area input {
            flex: 1;
            padding: clamp(10px, 2.8vw, 12px) clamp(14px, 3.5vw, 16px);
            background: #1a1a1a;
            border: 1px solid #2d2d2d;
            border-radius: 24px;
            color: #fff;
            font-size: clamp(14px, 3.8vw, 15px);
            outline: none;
            min-width: 0;
        }
        
        .input-area input:focus {
            border-color: #444;
        }
        
        .input-area input::placeholder {
            color: #666;
            font-size: clamp(13px, 3.5vw, 14px);
        }
        
        .input-area button {
            padding: clamp(10px, 2.8vw, 12px) clamp(20px, 5vw, 24px);
            background: #2d2d2d;
            border: none;
            border-radius: 24px;
            color: #fff;
            font-weight: 500;
            cursor: pointer;
            transition: 0.2s;
            font-size: clamp(13px, 3.5vw, 14px);
            white-space: nowrap;
        }
        
        .input-area button:hover {
            background: #3d3d3d;
        }
        
        .input-area button:active {
            transform: scale(0.98);
        }
        
        .typing {
            padding: 8px 24px;
            color: #666;
            font-size: clamp(11px, 2.8vw, 12px);
            font-style: italic;
        }
        
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0a0a0a;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #2d2d2d;
            border-radius: 3px;
        }
        
        @media (max-width: 768px) and (max-height: 600px) {
            .messages {
                max-height: calc(100vh - 140px);
            }
            
            .input-area {
                padding: 10px 16px;
            }
        }
    </style>
</head>
<body>
    <div class="app">
        <button class="menu-toggle" onclick="toggleSidebar()">☰</button>
        <div class="overlay" onclick="toggleSidebar()"></div>
        
        <div class="sidebar" id="sidebar">
            <div class="user">
                <div class="user-name">{{ username }}</div>
                <a href="/logout" class="logout">Выйти</a>
            </div>
            
            <div class="channels">
                <div class="channel active" onclick="switchChannel('general')">
                    <span style="margin-right: 10px;">💬</span>
                    Общий чат
                </div>
                
                <div class="divider">Личные сообщения</div>
                
                <div id="usersList">
                    {% for user in users %}
                    <div class="channel" id="user-{{ user }}" onclick="switchChannel('{{ user }}')">
                        <span class="online-status offline" id="status-{{ user }}"></span>
                        <span style="flex: 1;">{{ user }}</span>
                        <span class="badge" id="notify-{{ user }}" style="display: none;"></span>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="main">
            <div class="header" id="chatHeader">
                Общий чат
            </div>
            
            <div class="messages" id="chatMessages"></div>
            
            <div class="typing" id="typingIndicator" style="display: none;"></div>
            
            <div class="input-area">
                <input type="text" id="messageInput" 
                       placeholder="Сообщение..." 
                       autocomplete="off">
                <button onclick="sendMessage()">→</button>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        const username = '{{ username }}';
        let currentChannel = 'general';
        let currentUser = null;
        let typingTimeout = null;
        let unreadMessages = {};
        const displayedMessageIds = new Set();

        // ============ ФУНКЦИИ ДЛЯ КНОПОК ============
        
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.querySelector('.overlay');
            sidebar.classList.toggle('open');
            overlay.classList.toggle('show');
        }

        function switchChannel(channel) {
            document.querySelectorAll('.channel').forEach(el => {
                el.classList.remove('active');
            });
            
            if (window.innerWidth <= 768) {
                toggleSidebar();
            }
            
            if (channel === 'general') {
                document.getElementById('chatHeader').innerHTML = 'Общий чат';
                currentChannel = 'general';
                currentUser = null;
                
                document.getElementById('chatMessages').innerHTML = '';
                displayedMessageIds.clear();
                
                fetch('/api/messages')
                    .then(res => res.json())
                    .then(messages => {
                        messages.forEach(msg => {
                            const msgId = `${msg.id}-${msg.from}-${msg.time}`;
                            displayedMessageIds.add(msgId);
                            displayMessage(msg);
                        });
                    });
            } else {
                document.getElementById('chatHeader').innerHTML = `${channel}`;
                currentChannel = 'private';
                currentUser = channel;
                document.getElementById(`user-${channel}`).classList.add('active');
                
                const badge = document.getElementById(`notify-${channel}`);
                if (badge) badge.style.display = 'none';
                
                document.getElementById('chatMessages').innerHTML = '';
                displayedMessageIds.clear();
                
                fetch(`/api/private/${channel}`)
                    .then(res => res.json())
                    .then(messages => {
                        messages.forEach(msg => {
                            const msgId = `${msg.id}-${msg.from}-${msg.time}-private`;
                            displayedMessageIds.add(msgId);
                            displayPrivateMessage(msg);
                        });
                    });
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            
            if (!text) return;
            
            if (currentChannel === 'general') {
                socket.emit('send_message', { text: text });
            } else {
                socket.emit('send_private', {
                    to: currentUser,
                    text: text
                });
            }
            
            input.value = '';
        }
        
        // ============ ОТОБРАЖЕНИЕ СООБЩЕНИЙ ============
        
        function displayMessage(msg) {
            const messagesDiv = document.getElementById('chatMessages');
            
            const msgId = `${msg.id}-${msg.from}-${msg.time}`;
            if (displayedMessageIds.has(msgId)) return;
            displayedMessageIds.add(msgId);
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${msg.from === username ? 'own' : ''}`;
            
            messageDiv.innerHTML = `
                ${msg.from !== username ? `<div class="message-sender">${escapeHtml(msg.from)}</div>` : ''}
                <div class="message-bubble">${escapeHtml(msg.text)}</div>
                <div class="message-time">${msg.time || new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
            `;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function displayPrivateMessage(msg) {
            if (currentUser === msg.from || currentUser === msg.to) {
                const messagesDiv = document.getElementById('chatMessages');
                
                const msgId = `${msg.id}-${msg.from}-${msg.time}-private`;
                if (displayedMessageIds.has(msgId)) return;
                displayedMessageIds.add(msgId);
                
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${msg.from === username ? 'own' : ''}`;
                
                messageDiv.innerHTML = `
                    ${msg.from !== username ? `<div class="message-sender">${escapeHtml(msg.from)}</div>` : ''}
                    <div class="message-bubble">${escapeHtml(msg.text)}</div>
                    <div class="message-time">${msg.time || new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                `;
                
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        }
        
        // ============ СОКЕТ-СОБЫТИЯ ============
        
        socket.on('new_message', function(msg) {
            if (currentChannel === 'general') {
                displayMessage(msg);
            }
        });
        
        socket.on('new_private', function(msg) {
            displayPrivateMessage(msg);
            
            if (currentUser !== msg.from && msg.from !== username) {
                fetch('/api/unread')
                    .then(res => res.json())
                    .then(unread => {
                        unreadMessages = unread;
                        const badge = document.getElementById(`notify-${msg.from}`);
                        if (badge && unread[msg.from]) {
                            badge.style.display = 'inline';
                            badge.textContent = unread[msg.from];
                        }
                    });
            }
        });
        
        socket.on('users_update', function(users) {
            const usersList = document.getElementById('usersList');
            usersList.innerHTML = '';
            
            users.forEach(user => {
                if (user.username !== username) {
                    const div = document.createElement('div');
                    div.className = 'channel';
                    div.id = `user-${user.username}`;
                    div.onclick = () => switchChannel(user.username);
                    div.innerHTML = `
                        <span class="online-status ${user.online ? 'online' : 'offline'}" 
                              id="status-${user.username}"></span>
                        <span style="flex: 1;">${user.username}</span>
                        <span class="badge" id="notify-${user.username}" 
                              style="display: ${unreadMessages[user.username] ? 'inline' : 'none'};">
                            ${unreadMessages[user.username] || ''}
                        </span>
                    `;
                    usersList.appendChild(div);
                }
            });
        });
        
        socket.on('user_online', function(data) {
            const statusEl = document.getElementById(`status-${data.username}`);
            if (statusEl) statusEl.className = 'online-status online';
        });
        
        socket.on('user_offline', function(data) {
            const statusEl = document.getElementById(`status-${data.username}`);
            if (statusEl) statusEl.className = 'online-status offline';
        });
        
        socket.on('unread_update', function(unread) {
            unreadMessages = unread;
            for (let [user, count] of Object.entries(unread)) {
                const badge = document.getElementById(`notify-${user}`);
                if (badge) {
                    badge.style.display = 'inline';
                    badge.textContent = count;
                }
            }
        });
        
        socket.on('user_typing', function(data) {
            if (currentChannel === 'general' && data.username !== username && data.is_typing) {
                const indicator = document.getElementById('typingIndicator');
                indicator.style.display = 'block';
                indicator.innerHTML = `${data.username} печатает...`;
                
                clearTimeout(typingTimeout);
                typingTimeout = setTimeout(() => {
                    indicator.style.display = 'none';
                }, 1500);
            } else if (!data.is_typing) {
                document.getElementById('typingIndicator').style.display = 'none';
            }
        });
        
        socket.on('user_typing_private', function(data) {
            if (currentUser === data.username && data.is_typing) {
                const indicator = document.getElementById('typingIndicator');
                indicator.style.display = 'block';
                indicator.innerHTML = `${data.username} печатает...`;
                
                clearTimeout(typingTimeout);
                typingTimeout = setTimeout(() => {
                    indicator.style.display = 'none';
                }, 1500);
            } else if (!data.is_typing) {
                document.getElementById('typingIndicator').style.display = 'none';
            }        });
        
        // ============ ИНДИКАТОР ПЕЧАТАНИЯ ============
        
        document.getElementById('messageInput').addEventListener('input', function() {
            clearTimeout(typingTimeout);
            
            if (currentChannel === 'general') {
                socket.emit('typing', { to: 'general', is_typing: true });
            } else {
                socket.emit('typing', { to: currentUser, is_typing: true });
            }
            
            typingTimeout = setTimeout(() => {
                if (currentChannel === 'general') {
                    socket.emit('typing', { to: 'general', is_typing: false });
                } else {
                    socket.emit('typing', { to: currentUser, is_typing: false });
                }
            }, 1000);
        });
        
        // ============ ОТПРАВКА ПО ENTER ============
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // ============ ХЕЛПЕРЫ ============
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // ============ СВАЙП ДЛЯ МОБИЛОК ============
        
        let touchStartX = 0;
        document.addEventListener('touchstart', e => {
            touchStartX = e.touches[0].clientX;
        });

        document.addEventListener('touchend', e => {
            const touchEndX = e.changedTouches[0].clientX;
            const sidebar = document.getElementById('sidebar');
            const overlay = document.querySelector('.overlay');
            
            if (touchStartX < 30 && touchEndX > 100) {
                sidebar.classList.add('open');
                overlay.classList.add('show');
            }
            
            if (touchStartX > 100 && touchEndX < 30) {
                sidebar.classList.remove('open');
                overlay.classList.remove('show');
            }
        });
        
        // ============ ФОКУС ДЛЯ МОБИЛОК ============
        
        document.getElementById('messageInput').addEventListener('focus', function() {
            if (window.innerWidth <= 768) {
                setTimeout(() => {
                    window.scrollTo(0, document.body.scrollHeight);
                }, 300);
            }
        });
        
        // ============ ПРОВЕРКА ПОДКЛЮЧЕНИЯ ============
        
        socket.on('connect', function() {
            console.log('✅ WebSocket подключен');
        });
        
        socket.on('connect_error', function(error) {
            console.error('❌ WebSocket ошибка:', error);
        });
        
        socket.on('disconnect', function() {
            console.log('❌ WebSocket отключен');
        });
        
        // ============ ИНИЦИАЛИЗАЦИЯ ============
        
        console.log('✅ Чат загружен, пользователь:', username);
        console.log('📁 Текущий канал:', currentChannel);
        
        // ============ ПРЕДОТВРАЩЕНИЕ ДУБЛЕЙ СООБЩЕНИЙ ============
        
        // Очищаем Set при перезагрузке страницы
        window.addEventListener('beforeunload', function() {
            displayedMessageIds.clear();
        });
        
    </script>
</body>
</html>