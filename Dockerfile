# syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD ["python3", "src/youtooler.py", "--url", "https://youtube.com/watch?v=AhFdp8mJE_U"]
