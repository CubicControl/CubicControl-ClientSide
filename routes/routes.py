import datetime
from typing import Optional

import requests
from flask import render_template, jsonify, Blueprint, request, session, redirect, url_for
from wakeonlan import send_magic_packet

from utils.config import TARGET_IP_ADDRESS, TARGET_FLASK_SERVER_PORT, TARGET_MAC_ADDRESS, LOGIN_USERNAME, \
    LOGIN_PASSWORD, AUTH_KEY
from utils.wrappers import handle_timeout, login_required

auth_key_header = {'Authorization': f'Bearer {AUTH_KEY}'}
bp = Blueprint('routes', __name__)

last_manual_start: Optional[datetime.datetime] = None
@bp.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    return render_template("index.html")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('routes.index'))
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    return render_template('login.html')

@bp.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({"message": "Logged out successfully"}), 200

@bp.route('/status', methods=['GET'])
@handle_timeout
@login_required
def status():
    try:
        response = requests.get(
            f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/status",
            headers=auth_key_header,
            timeout=5
        )
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Unable to connect to the server"}), 500

@bp.route('/wake', methods=['POST'])
@handle_timeout
@login_required
def wake():
    send_magic_packet(TARGET_MAC_ADDRESS, ip_address=TARGET_IP_ADDRESS)
    return jsonify({"message": "WOL packet sent successfully! Machine is starting..."}), 200

@bp.route('/start', methods=['POST'])
@handle_timeout
@login_required
def start():
    global last_manual_start
    if last_manual_start and (datetime.datetime.now() - last_manual_start).total_seconds() < 10:
        return jsonify({"error": "Server was started too recently"}), 400

    try:
        response = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/start", headers=auth_key_header)
        if response.status_code == 200:
            last_manual_start = datetime.datetime.now()
        return jsonify({"message": response.text }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Unable to connect to the server: {e}"}), 500

@bp.route('/stop', methods=['POST'])
@handle_timeout
@login_required
def stop():
    try:
        response = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/stop", headers=auth_key_header)
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Unable to connect to the server: {e}"}), 500


@bp.route('/restart', methods=['POST'])
@handle_timeout
@login_required
def restart():
    try:
        response = requests.post(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/restart", headers=auth_key_header)
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Unable to connect to the server: {e}"}), 500

