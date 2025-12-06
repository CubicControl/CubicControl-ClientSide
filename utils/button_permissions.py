import os

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}

def _get_bool_env(var_name: str, default: bool = True) -> bool:
    value = os.environ.get(var_name)
    if value is None:
        return default
    lowered = value.strip().lower()
    if lowered in _TRUE_VALUES:
        return True
    if lowered in _FALSE_VALUES:
        return False
    # If invalid value, fall back to default to avoid surprises
    return default

ALLOW_WAKE = _get_bool_env("ALLOW_WAKE", True)
ALLOW_START = _get_bool_env("ALLOW_START", True)
ALLOW_STOP = _get_bool_env("ALLOW_STOP", False)
ALLOW_RESTART = _get_bool_env("ALLOW_RESTART", False)

_BUTTON_MAP = {
    "wake": ALLOW_WAKE,
    "start": ALLOW_START,
    "stop": ALLOW_STOP,
    "restart": ALLOW_RESTART,
}

def is_allowed(action: str) -> bool:
    """Return whether the given action is permitted based on static flags."""
    return _BUTTON_MAP.get(action, False)

BUTTON_PERMISSIONS = _BUTTON_MAP
