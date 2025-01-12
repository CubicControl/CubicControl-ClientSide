import requests
from ping3 import ping
import os

# Your PC's IP address
TARGET_IP_ADDRESS = os.environ.get('TARGET_IP_ADDRESS_SERVER')
TARGET_FLASK_SERVER_PORT = os.environ.get('TARGET_FLASK_SERVER_PORT')

response_time = ping(f"{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}", timeout=2)
if response_time is not None:
    print(f"Response time: {response_time} ms")
    response = requests.get(f"http://{TARGET_IP_ADDRESS}:{TARGET_FLASK_SERVER_PORT}/status")
    print(response.text)
else:
    print("PC is off!")