import logging
from functools import wraps

import requests
from flask import jsonify, request, session, redirect, url_for

from utils.config import AUTH_KEY

logger = logging.getLogger(__name__)

def handle_timeout(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.Timeout:
            return jsonify({"error": "Machine is not reachable"}), 504
        except requests.exceptions.RequestException as exc:
            logger.warning("Request to backend failed: %s", exc)
            return jsonify({"error": "Backend request failed"}), 502
    return decorated_function


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if auth_token != AUTH_KEY:
            return jsonify({"error": "Unauthorized, invalid token"}), 401
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function



