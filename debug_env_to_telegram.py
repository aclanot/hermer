import hashlib
import json
import os
import urllib.error
import urllib.request


def mask(value: str) -> str:
    if not value:
        return "❌ missing"
    if len(value) <= 12:
        return f"⚠️ short len={len(value)} repr={value!r}"
    digest = hashlib.sha256(value.encode()).hexdigest()[:12]
    return f"✅ len={len(value)} start={value[:6]}...end={value[-6:]} sha12={digest}"


def send_telegram(text: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_HOME_CHAT_ID") or os.environ.get("TELEGRAM_ALLOWED_USERS")

    if not token:
        print("TELEGRAM_BOT_TOKEN missing; cannot send Telegram debug.")
        return

    if not chat_id:
        print("TELEGRAM_HOME_CHAT_ID / TELEGRAM_ALLOWED_USERS missing; cannot send Telegram debug.")
        return

    chat_id = chat_id.split(",")[0].strip()

    payload = {
        "chat_id": chat_id,
        "text": text[:3900],
        "parse_mode": "HTML",
    }

    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        print(response.read().decode("utf-8"))


def test_sub2api() -> str:
    base_url = os.environ.get("OPENAI_BASE_URL", "https://sub2api-production-d36c.up.railway.app/v1").rstrip("/")
    api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        return "❌ Sub2API test skipped: OPENAI_API_KEY missing"

    payload = {
        "model": "gpt-5.5",
        "input": "Say OK only.",
    }

    request = urllib.request.Request(
        f"{base_url}/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", errors="replace")
            return f"✅ Sub2API test OK: HTTP {response.status}\nBody: {body[:500]}"
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        return f"❌ Sub2API test failed: HTTP {error.code}\nBody: {body[:700]}"
    except Exception as error:
        return f"❌ Sub2API test error: {type(error).__name__}: {error}"


def main() -> None:
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")

    suspicious = []
    if openai_key.startswith("{"):
        suspicious.append("⚠️ OPENAI_API_KEY looks like JSON, not raw key.")
    if openai_key.startswith('"') or openai_key.endswith('"'):
        suspicious.append("⚠️ OPENAI_API_KEY has quotes.")
    if openai_key != openai_key.strip():
        suspicious.append("⚠️ OPENAI_API_KEY has leading/trailing whitespace.")
    if telegram_token.startswith("{"):
        suspicious.append("⚠️ TELEGRAM_BOT_TOKEN looks like JSON.")

    report = "\n".join([
        "🧪 <b>Hermes Railway Env Debug</b>",
        "",
        f"OPENAI_BASE_URL: <code>{os.environ.get('OPENAI_BASE_URL', 'missing')}</code>",
        f"OPENAI_API_KEY: <code>{mask(openai_key)}</code>",
        f"TELEGRAM_BOT_TOKEN: <code>{mask(telegram_token)}</code>",
        f"TELEGRAM_ALLOWED_USERS: <code>{os.environ.get('TELEGRAM_ALLOWED_USERS', 'missing')}</code>",
        f"TELEGRAM_HOME_CHAT_ID: <code>{os.environ.get('TELEGRAM_HOME_CHAT_ID', 'missing')}</code>",
        "",
        "\n".join(suspicious) if suspicious else "✅ No obvious env formatting issues.",
        "",
        test_sub2api(),
    ])

    send_telegram(report)


if __name__ == "__main__":
    main()