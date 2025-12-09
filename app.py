import datetime
import secrets
import os

from flask import Flask
from flask_cors import CORS

from routes.routes import bp
from utils.extensions import socketio
from ws import status_events  # noqa: F401 ensures websocket handlers are registered

app = Flask(__name__)
secret_key = secrets.token_hex(16)
# Persist the secret key across restarts to avoid invalidating sessions.
persisted_secret_key = os.environ.get('SECRET_KEY')
if not persisted_secret_key:
    secret_file_path = os.path.join(app.instance_path, 'secret_key')
    os.makedirs(app.instance_path, exist_ok=True)
    if os.path.exists(secret_file_path):
        with open(secret_file_path, 'r') as secret_file:
            persisted_secret_key = secret_file.read().strip()
    else:
        persisted_secret_key = secrets.token_hex(16)
        with open(secret_file_path, 'w') as secret_file:
            secret_file.write(persisted_secret_key)

app.config['SECRET_KEY'] = persisted_secret_key
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
CORS(app, resources={r"/*": {"origins": ["https://serverwebsite-z5my.onrender.com/"]}})
socketio.init_app(app, cors_allowed_origins="*")

app.register_blueprint(bp)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False, allow_unsafe_werkzeug=True)
