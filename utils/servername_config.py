import os

def get_server_name():
    """Return server name from env var, else file, else default."""
    env_value = os.environ.get('SERVER_NAME')
    default_name = 'Change Me in Environment Variables'

    if env_value is not None and env_value.strip():
        return env_value.strip()

    return default_name
