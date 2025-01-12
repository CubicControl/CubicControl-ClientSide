import datetime
import os

from flask import Flask, request, jsonify, render_template
from wakeonlan import send_magic_packet
import requests
from functools import wraps

app = Flask(__name__)

AUTH_KEY = os.environ.get('AUTHKEY_SERVER_WEBSITE') # Secure key for authentication
TARGET_MAC_ADDRESS = os.environ.get('TARGET_MAC_ADDRESS_SERVER') # Your PC's MAC address for Wake On Lan
TARGET_IP_ADDRESS = os.environ.get('TARGET_IP_ADDRESS_SERVER') # Your PC's IP address
TARGET_FLASK_SERVER_PORT = os.environ.get('TARGET_FLASK_SERVER_PORT')
last_manual_start = 0

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
def get_auth_key():
    return request.headers.get('Authorization')
@app.route('/')
def index():
    return render_template('index.html', auth_key=AUTH_KEY)

@app.route('/status', methods=['GET'])
@handle_timeout
def status():
    ping_server = requests.get(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/status", timeout=5)
    if ping_server.status_code in [200, 205, 206, 207]:
        return ping_server.text, ping_server.status_code
    else:
        return jsonify({"status": "off"}), 500

@app.route('/wake', methods=['POST'])
@handle_timeout
def wake():
    auth_key = get_auth_key()
    if auth_key != AUTH_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    send_magic_packet(TARGET_MAC_ADDRESS, ip_address=TARGET_IP_ADDRESS)
    return jsonify({"message": "WOL packet sent successfully! Machine is starting..."}), 200

@app.route('/stop', methods=['POST'])
@handle_timeout
def stop():
    auth_key = get_auth_key()
    if auth_key != AUTH_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    stop_request = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/stop")
    if stop_request.status_code == 400:
        return jsonify({"message": stop_request.text}), 400
    elif stop_request.status_code == 200:
        return jsonify({"message": stop_request.text}), 200
    elif stop_request.status_code == 302:
        return jsonify({"message": "Server is still booting, please wait..."}), 302
    elif stop_request.status_code == 305:
        return jsonify({"message": "Server is restarting, please wait..."}), 305
    elif stop_request.status_code == 500:
        return jsonify({"error": "Failed to stop server on server side"}), 500
    else:
        return jsonify({"error": "Failed to stop server via client side"}), 500

@app.route('/start', methods=['POST'])
@handle_timeout
def start():
    global last_manual_start
    auth_key = get_auth_key()
    if auth_key != AUTH_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    if last_manual_start != 0:
        time_since_last_manual_start = datetime.datetime.now() - last_manual_start
        if time_since_last_manual_start.total_seconds() < 5:
            return jsonify({"error": "Server was started too recently"}), 400

    post_request = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/start")
    if post_request.status_code == 400:
        return jsonify({"message": post_request.text}), 400
    elif post_request.status_code == 200:
        last_manual_start = datetime.datetime.now()
        return jsonify({"message": post_request.text}), 200
    elif post_request.status_code == 500:
        return jsonify({"error": "Failed to start server on server side"}), 500
    else:
        return jsonify({"error": "Failed to start server via client side"}), 500

@app.route('/restart', methods=['POST'])
@handle_timeout
def restart():
    auth_key = get_auth_key()
    if auth_key != AUTH_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    restart_request = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/restart")
    if restart_request.status_code == 400:
        return jsonify({"message": restart_request.text}), 400
    elif restart_request.status_code == 302:
        return jsonify({"message": "Server is still booting, please wait..."}), 302
    elif restart_request.status_code == 200:
        return jsonify({"message": restart_request.text}), 200
    elif restart_request.status_code == 206:
        return jsonify({"message": "Server is restarting, please wait..."}), 206
    elif restart_request.status_code == 500:
        return jsonify({"error": "Failed to restart server on server side"}), 500
    else:
        return jsonify({"error": "Failed to restart server via client side"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')