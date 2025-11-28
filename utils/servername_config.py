# Utility function to read server name from file
import os


def get_server_name():
    filename = 'servername.txt'
    default_name = 'Server name HERE. Change in servername.txt'
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(default_name)
        return default_name
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip() or default_name