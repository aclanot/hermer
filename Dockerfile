FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade hermes-agent

COPY config.yaml /app/config.yaml
COPY send_telegram_keyboard.py /app/send_telegram_keyboard.py
COPY debug_env_to_telegram.py /app/debug_env_to_telegram.py
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]