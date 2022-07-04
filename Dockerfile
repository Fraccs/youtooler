# syntax=docker/dockerfile:1
FROM python:3.10-alpine

WORKDIR /
RUN apk update

# Install TOR
RUN apk add tor

# Install Firefox
RUN apk add firefox-esr

# Install geckodriver
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk
RUN apk add glibc-2.30-r0.apk
RUN apk add glibc-bin-2.30-r0.apk
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin

# Install Python requirements
COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Install youtooler package
RUN pip3 install -e .

CMD ["python3", "src/youtooler.py", "--url", "https://www.youtube.com/watch?v=AhFdp8mJE_U"]
