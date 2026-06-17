#!/usr/bin/env bash
set -e

python /app/send_telegram_keyboard.py || true

exec hermes gateway