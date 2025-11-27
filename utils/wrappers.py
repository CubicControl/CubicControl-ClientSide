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
        raw_header = request.headers.get('Authorization', '')
        auth_token = raw_header.replace('Bearer ', '')
        if auth_token:
            if auth_token != AUTH_KEY:
                logger.warning("Authorization token mismatch against AUTHKEY_SERVER_WEBSITE")
                return jsonify({"error": "Unauthorized, invalid token"}), 403
            return f(*args, **kwargs)

        if session.get('logged_in'):
            logger.debug("Authenticated via session; Authorization header missing")
            return f(*args, **kwargs)

        logger.warning("Authorization header missing on protected endpoint")
        return jsonify({"error": "Unauthorized, missing Authorization: Bearer token"}), 403
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function



