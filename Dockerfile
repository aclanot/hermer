FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir hermes-agent

RUN mkdir -p /root/.hermes
COPY config.toml /root/.hermes/config.toml

CMD ["hermes", "gateway"]