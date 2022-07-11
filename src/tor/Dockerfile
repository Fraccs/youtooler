FROM python:3.10-alpine

WORKDIR /tor

RUN apk update
RUN apk add tor

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["start.py"]
