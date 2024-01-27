import socket
import time

import requests

from flask import Flask
from icecream import ic

app = Flask(__name__)


def is_bot_responding(bot_token, chat_id):
    message_text = f"Health check at {time.time()}"
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    get_updates_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    # Send a message to the bot
    response = requests.post(
        send_message_url, data={"chat_id": chat_id, "text": message_text}
    )
    ic(response)
    ic(response.json())
    # Wait for a bit to give the bot time to respond
    time.sleep(5)

    # Check the bot's updates
    response = requests.get(get_updates_url)
    updates = response.json()

    ic(updates)
    # Check if the bot's latest message matches the health check message
    for update in reversed(updates["result"]):  # Start with the most recent messages
        if update["message"]["text"] == message_text:
            return True

    return False


def check_telegram_bot(token, chat_id):
    try:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
        return response.status_code == 200
        # if response.status_code == 200:
        #     return is_bot_responding(token, chat_id=chat_id)

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
