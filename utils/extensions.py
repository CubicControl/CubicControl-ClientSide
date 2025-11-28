from flask_socketio import SocketIO


# Shared Socket.IO instance used across the application and websocket event modules.
socketio = SocketIO(async_mode="threading", cors_allowed_origins="*")