import datetime
import os
from typing import Optional

from flask import Flask, request, jsonify, render_template
from wakeonlan import send_magic_packet
import requests
from functools import wraps
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

AUTH_KEY = os.environ.get('AUTHKEY_SERVER_WEBSITE') # Secure key for authentication
TARGET_MAC_ADDRESS = os.environ.get('TARGET_MAC_ADDRESS_SERVER') # Your PC's MAC address for Wake On Lan
TARGET_IP_ADDRESS = os.environ.get('TARGET_IP_ADDRESS_SERVER') # Your PC's IP address
TARGET_FLASK_SERVER_PORT = os.environ.get('TARGET_FLASK_SERVER_PORT')
last_manual_start: Optional[datetime.datetime] = None

def handle_timeout(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.Timeout:
            return jsonify({"status": "off", "error": "Machine is not reachable"}), 500
        except Exception as e:
            return jsonify({"status": "off", "error": str(e)}), 500
    return decorated_function

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_key = get_auth_key()
        if not is_authorized(auth_key):
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function
def get_auth_key():
    return request.headers.get('Authorization', '').replace('Bearer ', '')

def is_authorized(auth_key):
    return auth_key == AUTH_KEY
@app.route('/')
def index():
    return render_template('index.html', auth_key=AUTH_KEY)

@app.route('/status', methods=['GET'])
@handle_timeout
def status():
    try:
        response = requests.get(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/status", timeout=5)
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "off", "error": "Unable to connect to the server"}), 500


@app.route('/wake', methods=['POST'])
@handle_timeout
@require_auth
def wake():
    send_magic_packet(TARGET_MAC_ADDRESS, ip_address=TARGET_IP_ADDRESS)
    return jsonify({"message": "WOL packet sent successfully! Machine is starting..."}), 200

@app.route('/stop', methods=['POST'])
@handle_timeout
@require_auth
def stop():
    try:
        response = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/stop")
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "off", "error": f"Unable to connect to the server: {e}"}), 500

@app.route('/start', methods=['POST'])
@handle_timeout
@require_auth
def start():
    global last_manual_start
    if last_manual_start and (datetime.datetime.now() - last_manual_start).total_seconds() < 5:
        return jsonify({"error": "Server was started too recently"}), 400

    try:
        response = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/start")
        if response.status_code == 200:
            last_manual_start = datetime.datetime.now()
        return jsonify({"message": response.text }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "off", "error": f"Unable to connect to the server: {e}"}), 500

@app.route('/restart', methods=['POST'])
@handle_timeout
@require_auth
def restart():
    try:
        response = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/restart")
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "off", "error": f"Unable to connect to the server: {e}"}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0')