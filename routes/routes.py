import datetime
from typing import Optional

import requests
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from wakeonlan import send_magic_packet

from utils.backend import get_status, post_action
from utils.config import LOGIN_PASSWORD, LOGIN_USERNAME, TARGET_IP_ADDRESS, TARGET_MAC_ADDRESS
from utils.wrappers import handle_timeout, login_required, require_auth
from utils.state import load_last_manual_start, save_last_manual_start
from secrets import compare_digest

bp = Blueprint('routes', __name__)

last_manual_start: Optional[datetime.datetime] = load_last_manual_start()
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
        if username == LOGIN_USERNAME and compare_digest(password, LOGIN_PASSWORD):
            session['logged_in'] = True
            return redirect(url_for('routes.index'))
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    return render_template('login.html')

@bp.route('/logout', methods=['POST'])
@login_required
@require_auth
def logout():
    session.pop('logged_in', None)
    return jsonify({"message": "Logged out successfully"}), 200


@bp.route('/status', methods=['GET'])
@handle_timeout
@login_required
@require_auth
def status():
    try:
        response = get_status()
        if response.status_code == 403:
            return jsonify({"error": f"Unauthorized, invalid token: {response.text}"}), 403
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"error": "Unable to connect to the server", "host_status": "offline"}), 500


@bp.route('/wake', methods=['POST'])
@handle_timeout
@login_required
@require_auth
def wake():
    send_magic_packet(TARGET_MAC_ADDRESS, ip_address=TARGET_IP_ADDRESS)
    return jsonify({"message": "WOL packet sent successfully! Machine is starting..."}), 200

@bp.route('/start', methods=['POST'])
@handle_timeout
@login_required
@require_auth
def start():
    global last_manual_start
    if last_manual_start and (datetime.datetime.now() - last_manual_start).total_seconds() < 10:
        return jsonify({"error": "Server was started too recently"}), 400

    try:
        response = post_action("/start")
        if response.status_code == 200:
            last_manual_start = datetime.datetime.now()
            save_last_manual_start(last_manual_start)
        return jsonify({"message": response.text }), response.status_code
    except requests.exceptions.ConnectTimeout:
        return jsonify({"error": "Unable to connect to the server: Connection timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@bp.route('/stop', methods=['POST'])
@handle_timeout
@login_required
@require_auth
def stop():
    try:
        response = post_action("/stop")
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.ConnectTimeout:
        return jsonify({"error": "Unable to connect to the server: Connection timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@bp.route('/restart', methods=['POST'])
@handle_timeout
@login_required
@require_auth
def restart():
    try:
        response = post_action("/restart")
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.ConnectTimeout:
        return jsonify({"error": "Unable to connect to the server: Connection timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

