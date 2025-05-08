from flask import Flask, render_template
from flask_socketio import SocketIO, send

# websocket -> tunel
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

#function for send a message
@socketio.on("message")
def message_management(message):
    send(message, broadcast=True)

# create first page = first route.
@app.route("/")

def homepage():
    return render_template("index.html")

socketio.run(app, host="localhost")