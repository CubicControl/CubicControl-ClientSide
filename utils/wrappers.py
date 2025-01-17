import os
from functools import wraps

import requests
from flask import jsonify, request, session, redirect, url_for

from utils.config import AUTH_KEY


def handle_timeout(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.Timeout:
            return jsonify({"error": "Machine is not reachable"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return decorated_function

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if auth_token != AUTH_KEY:
            return jsonify({"error": "Unauthorized, invalid token"}), 401
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function



