# NOTE: This hash is pinned to avoid version and environment differences.
FROM python:3.14.6-slim-trixie@sha256:63a4c7f612a00f92042cbdcc7cdc6a306f38485af0a200b9c89de7d9b1607d15

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            gcc build-essential socat && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --chmod=444 server.py .
RUN mkdir /app/work && chmod 777 /app/work

USER nobody:nogroup

CMD ["socat", "-T60", "TCP-L:1337,fork,reuseaddr", "EXEC:'python3 -u server.py',stderr"]
