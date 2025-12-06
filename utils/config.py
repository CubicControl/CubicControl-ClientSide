import os

def _require_env(var_name: str) -> str:
    value = os.environ.get(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value

# Local testing values
AUTH_KEY = "SECRETKEYSPIRIT"
TARGET_MAC_ADDRESS = "24-4B-FE-DE-E2-8C"
TARGET_IP_ADDRESS = "jmgaming.chickenkiller.com"
LOGIN_USERNAME = _require_env('LOGIN_USERNAME')
LOGIN_PASSWORD = _require_env('LOGIN_PASSWORD')

# Production values from environment
# AUTH_KEY = _require_env('AUTHKEY_SERVER_WEBSITE')
# TARGET_MAC_ADDRESS = _require_env('TARGET_MAC_ADDRESS_SERVER')
# TARGET_IP_ADDRESS = _require_env('TARGET_IP_ADDRESS_SERVER')
# TARGET_FLASK_SERVER_PORT = _require_env('TARGET_FLASK_SERVER_PORT')
# LOGIN_USERNAME = _require_env('LOGIN_USERNAME')
# LOGIN_PASSWORD = _require_env('LOGIN_PASSWORD')
