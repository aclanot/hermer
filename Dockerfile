FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade hermes-agent

RUN mkdir -p /root/.hermes

COPY config.yaml /app/config.yaml
COPY config.yaml /root/.hermes/config.yaml
COPY send_telegram_keyboard.py /app/send_telegram_keyboard.py
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]