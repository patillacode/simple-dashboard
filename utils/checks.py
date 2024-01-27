import socket

import requests

from flask import Flask

app = Flask(__name__)


def check_telegram_bot(token, chat_id):
    try:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
        return response.status_code == 200

    except requests.RequestException as err:
        print(err)
        return False


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
    if service["name"].startswith("teamspeak"):
        active = check_teamspeak_server(service["status_url"])
        return active, None
    if service["name"].startswith("telegram-bot-"):
        active = check_telegram_bot(service["token"], service["chat_id"])
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
