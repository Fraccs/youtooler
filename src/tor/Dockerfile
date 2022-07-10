FROM python:3.10-alpine

WORKDIR /tor

RUN apk update
RUN apk add tor

COPY start.py .

ENTRYPOINT ["python"]

CMD ["start.py"]
