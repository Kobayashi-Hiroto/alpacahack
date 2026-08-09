FROM python:3.14.6-slim-trixie
WORKDIR /app
RUN apt-get update && apt-get install -yq socat
COPY server.py .

CMD ["socat", "-T5", "tcp-listen:1337,fork,reuseaddr", "exec:'python server.py',stderr,pty,ctty,setsid,echo=0"]
