import os

def _require_env(var_name: str) -> str:
    value = os.environ.get(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value


AUTH_KEY = _require_env('AUTHKEY_SERVER_WEBSITE')  # Secure key for authentication
TARGET_MAC_ADDRESS = _require_env('TARGET_MAC_ADDRESS_SERVER')  # Your PC's MAC address for Wake On Lan
# TARGET_IP_ADDRESS = "127.0.0.1" # For local testing
TARGET_IP_ADDRESS = _require_env('TARGET_IP_ADDRESS_SERVER')  # Your PC's IP address
TARGET_FLASK_SERVER_PORT = _require_env('TARGET_FLASK_SERVER_PORT')
LOGIN_USERNAME = _require_env('LOGIN_USERNAME')
LOGIN_PASSWORD = _require_env('LOGIN_PASSWORD')
