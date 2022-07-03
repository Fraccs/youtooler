# syntax=docker/dockerfile:1
FROM python:alpine3.10

WORKDIR /
RUN apk update

# Install TOR
RUN apk add tor

# Install Chrome

# Install Chromedriver

# Install Python requirements
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Install youtooler package
COPY . .
RUN pip3 install -e .

CMD ["python3", "src/youtooler.py", "--url", "https://www.youtube.com/watch?v=AhFdp8mJE_U"]
