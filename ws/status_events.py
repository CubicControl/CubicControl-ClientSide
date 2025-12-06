import logging
from threading import Lock
from typing import Dict, Optional

import requests
from flask_socketio import emit

from utils.backend import describe_status_code, get_status
from utils.extensions import socketio

logger = logging.getLogger(__name__)

_status_thread = None
_status_thread_lock = Lock()
_last_payload: Optional[Dict] = None


def _build_payload(status_code: Optional[int], message: str) -> Dict:
    return {
        "status_code": status_code,
        "status": describe_status_code(status_code),
        "message": message,
    }


def _fetch_status_payload() -> Dict:
    try:
        response = get_status()
        # Treat any HTTP error (including 5xx/502 when backend is down) as unreachable
        response.raise_for_status()
        message = response.text.strip() or "Machine is not reachable. It may be powered off."
        return _build_payload(response.status_code, message)
    except requests.exceptions.HTTPError as exc:
        code = exc.response.status_code if exc.response else None
        if code and code >= 500:
            return _build_payload(None, "Machine is not reachable. It may be powered off.")
        return _build_payload(code, f"Backend request failed (HTTP {code})")
    except requests.exceptions.Timeout:
        return _build_payload(None, "Machine is not reachable. It may be powered off.")
    except requests.exceptions.ConnectionError as exc:
        logger.warning("Machine is not reachable: %s", exc)
        return _build_payload(None, "Machine is not reachable. It may be powered off.")
    except requests.exceptions.RequestException as exc:
        logger.warning("Backend status check failed: %s", exc)
        return _build_payload(None, "Backend request failed")


def _status_publisher():
    global _last_payload
    while True:
        payload = _fetch_status_payload()
        if payload != _last_payload:
            socketio.emit("status_update", payload)
            _last_payload = payload
        socketio.sleep(5)


def _ensure_status_thread_running():
    global _status_thread
    with _status_thread_lock:
        if _status_thread is None:
            _status_thread = socketio.start_background_task(_status_publisher)


@socketio.on("connect")
def handle_connect():
    _ensure_status_thread_running()
    payload = _last_payload or _fetch_status_payload()
    emit("status_update", payload)


@socketio.on("request_status")
def handle_request_status():
    payload = _last_payload or _fetch_status_payload()
    emit("status_update", payload)
