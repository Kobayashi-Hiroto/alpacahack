FROM bash:5.3.9
RUN apk --no-cache add socat
COPY chal.sh flag.txt /
USER nobody:nogroup
CMD ["socat", "-T30", "tcp-listen:1337,fork,reuseaddr", "exec:'bash /chal.sh',stderr"]
