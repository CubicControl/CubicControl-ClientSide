from typing import Optional

import requests

from utils.config import AUTH_KEY, TARGET_FLASK_SERVER_PORT, TARGET_IP_ADDRESS


DEFAULT_TIMEOUT_SECONDS = 5
http_session = requests.Session()
auth_key_header = {"Authorization": f"Bearer {AUTH_KEY}"}


def _build_backend_url(path: str) -> str:
    return f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}{path}"


def get_status() -> requests.Response:
    return http_session.get(
        _build_backend_url("/status"),
        headers=auth_key_header,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )


def post_action(path: str) -> requests.Response:
    return http_session.post(
        _build_backend_url(path),
        headers=auth_key_header,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )


def describe_status_code(status_code: Optional[int]) -> str:
    if status_code == 200:
        return "online"
    if status_code == 205:
        return "booting"
    if status_code == 206:
        return "offline"
    if status_code == 207:
        return "restarting"
    if status_code == 403:
        return "unauthorized"
    if status_code == 500:
        return "server_error"
    return "unreachable"