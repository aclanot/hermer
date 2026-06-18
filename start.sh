#!/usr/bin/env bash
set -e

mkdir -p /root/.hermes
cp /app/config.yaml /root/.hermes/config.yaml

python /app/send_telegram_keyboard.py || true

exec hermes gateway