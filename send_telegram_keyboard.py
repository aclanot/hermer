import json
import os
import urllib.request

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ.get("TELEGRAM_HOME_CHAT_ID", "5984974221")

payload = {
    "chat_id": chat_id,
    "text": "🧭 Меню Hermes готове ✅",
    "reply_markup": {
        "keyboard": [
            [{"text": "/status"}, {"text": "/help"}, {"text": "/commands"}],
            [{"text": "/new main"}, {"text": "/sessions"}, {"text": "/usage"}],
            [{"text": "/model"}, {"text": "/reasoning show"}, {"text": "/fast status"}],
            [{"text": "/sethome"}, {"text": "/debug"}, {"text": "/restart"}],
            [{"text": "/footer off"}, {"text": "/stop"}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
        "is_persistent": True,
        "input_field_placeholder": "Обери команду або напиши повідомлення…",
    },
}

request = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(request, timeout=20) as response:
    print(response.read().decode("utf-8"))