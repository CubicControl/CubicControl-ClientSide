import os

AUTH_KEY = os.environ.get('AUTHKEY_SERVER_WEBSITE') # Secure key for authentication
TARGET_MAC_ADDRESS = os.environ.get('TARGET_MAC_ADDRESS_SERVER') # Your PC's MAC address for Wake On Lan
TARGET_IP_ADDRESS = os.environ.get('TARGET_IP_ADDRESS_SERVER') # Your PC's IP address
TARGET_FLASK_SERVER_PORT = os.environ.get('TARGET_FLASK_SERVER_PORT')
LOGIN_USERNAME = os.environ.get('LOGIN_USERNAME')
LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD')
