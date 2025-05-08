# 💬 Hashzap

Create a simple live chat using Flask and WebSockets, inspired by WhatsApp.  
Enables real-time communication between users connected to the same local server.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey)
![Socket.IO](https://img.shields.io/badge/WebSocket-Socket.IO-yellowgreen)
![HTML](https://img.shields.io/badge/UI-HTML%2FJS%2FCSS-blueviolet)

---

## 🚀 How to Use

### 1. Clone the repository and install dependencies

```bash
git clone https://github.com/yourusername/hashzap.git
cd hashzap
pip install -r requirements.txt
```

### 2. Run the application

```bash
python main.py
```

Open your browser and go to `http://localhost:5000` to start using the chat.

---

## 📂 Features

- Web interface allowing multiple users to chat in real-time
- Built with Flask as the web server and Flask-SocketIO for WebSocket communication
- Chat UI inspired by WhatsApp
- Messages are ephemeral — only connected users can see messages in real time

---

## 🖼️ Interface

- Input fields for username and message
- Dynamic message list
- Auto-scrolls to the latest message

---

## 🛠️ Built With

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [Socket.IO](https://socket.io/)
- [jQuery](https://jquery.com/)
- [HTML/CSS/JS](https://developer.mozilla.org/en-US/docs/Web)

---

## 📝 Notes

This project is ideal for learning about WebSockets and building real-time applications with Python.  
Messages are not stored (no database), making this a lightweight and ephemeral chat app.

---