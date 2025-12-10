import os

def _require_env(var_name: str) -> str:
    value = os.environ.get(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value

# Production values from environment
AUTH_KEY = _require_env('AUTH_KEY')
TARGET_MAC_ADDRESS = _require_env('TARGET_MAC_ADDRESS')
TARGET_IP_ADDRESS = _require_env('TARGET_IP_ADDRESS')
LOGIN_USERNAME = _require_env('LOGIN_USERNAME')
LOGIN_PASSWORD = _require_env('LOGIN_PASSWORD')
