import json
import os
import urllib.parse
import urllib.request

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ.get("TELEGRAM_HOME_CHAT_ID", "5984974221")

keyboard = [
    ["📊 Статус", "✨ Новий чат"],
    ["🗂 Сесії", "📈 Використання"],
    ["🤖 Модель", "⚡ Швидкий режим"],
    ["🧠 Reasoning", "❓ Допомога"],
    ["🧭 Усі команди", "🛑 Зупинити"],
]

payload = {
    "chat_id": chat_id,
    "text": "Меню Hermes готове ✅",
    "reply_markup": json.dumps({
        "keyboard": keyboard,
        "resize_keyboard": True,
        "one_time_keyboard": False,
        "is_persistent": True,
        "input_field_placeholder": "Оберіть дію…",
    }, ensure_ascii=False),
}

request = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=urllib.parse.urlencode(payload).encode(),
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    method="POST",
)

with urllib.request.urlopen(request, timeout=20) as response:
    print(response.read().decode())