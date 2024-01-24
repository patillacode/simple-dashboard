import socket

import requests

from flask import Flask

app = Flask(__name__)


def check_teamspeak_server(host, port=10011):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        return True

    except Exception as err:
        print(f"Something went wrong: {err}")
        return False

    finally:
        sock.close()


def check_service(service):
    if service["name"] == "TeamSpeak 3":
        active = check_teamspeak_server(service["status_url"])
        return active, None

    try:
        response = requests.request(
            service["method"], service["status_url"], headers=service["headers"]
        )
        active = response.status_code == service["expected_status"]
        return active, response.status_code

    except requests.RequestException as err:
        print(err)
        return (False, None)
