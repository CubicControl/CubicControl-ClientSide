import datetime
import re
from secrets import compare_digest
from typing import Optional

import requests
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from wakeonlan import send_magic_packet

from utils.backend import get_status, post_action
from utils.button_permissions import BUTTON_PERMISSIONS, is_allowed
from utils.config import LOGIN_PASSWORD, LOGIN_USERNAME, TARGET_IP_ADDRESS, TARGET_MAC_ADDRESS
from utils.servername_config import get_server_name
from utils.state import load_last_manual_start, save_last_manual_start
from utils.wrappers import handle_timeout, login_required, require_auth

MAC_REGEX = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
bp = Blueprint('routes', __name__)

CONNECTION_TIMEOUT_ERROR_MESSAGE = "Unable to connect to the server: Connection timed out"

def _deny_action():
    return jsonify({"error": "Action not allowed"}), 403

last_manual_start: Optional[datetime.datetime] = load_last_manual_start()
@bp.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    return render_template("index.html", server_name=get_server_name(), button_permissions=BUTTON_PERMISSIONS)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('routes.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == LOGIN_USERNAME and compare_digest(password, LOGIN_PASSWORD):
            session['logged_in'] = True
            return redirect(url_for('routes.index'))
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    return render_template('login.html', server_name=get_server_name())

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
@require_auth
def logout():
    session.pop('logged_in', None)
    if request.method == 'POST':
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return redirect(url_for('routes.login'))


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
@login_required
@require_auth
def wake():
    if not is_allowed("wake"):
        return _deny_action()
    if not re.match(MAC_REGEX, TARGET_MAC_ADDRESS):
        return jsonify({"error": "Invalid MAC address format"}), 400
    try:
        send_magic_packet(TARGET_MAC_ADDRESS, ip_address=TARGET_IP_ADDRESS)
        return jsonify({"message": "Wake command sent successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500

@bp.route('/start', methods=['POST'])
@handle_timeout
@login_required
@require_auth
def start():
    if not is_allowed("start"):
        return _deny_action()
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
        return jsonify({"error": CONNECTION_TIMEOUT_ERROR_MESSAGE}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@bp.route('/stop', methods=['POST'])
@handle_timeout
@login_required
@require_auth
def stop():
    if not is_allowed("stop"):
        return _deny_action()
    try:
        response = post_action("/stop")
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.ConnectTimeout:
        return jsonify({"error": CONNECTION_TIMEOUT_ERROR_MESSAGE}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@bp.route('/restart', methods=['POST'])
@handle_timeout
@login_required
@require_auth
def restart():
    if not is_allowed("restart"):
        return _deny_action()
    try:
        response = post_action("/restart")
        return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.ConnectTimeout:
        return jsonify({"error": "Unable to connect to the server: Connection timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
