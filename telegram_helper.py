import requests
from config import BOT_TOKEN, CHAT_ID

# ==========================
# SEND TELEGRAM MESSAGE
# ==========================

def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    return response


# ==========================
# SEND FILE
# ==========================

def send_file(file_path):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(file_path, "rb") as file:

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID
            },
            files={
                "document": file
            }
        )

    return response