FROM alpine:latest

WORKDIR /tor

RUN apk update & \
    apk add tor

COPY start.sh .

ENTRYPOINT ["/bin/sh"]

CMD ["start.sh"]
