FROM python:3.10.5-slim-buster

WORKDIR /app

# Installing python requirements
COPY . .
RUN pip install -r requirements.txt

# Installing youtooler package locally
RUN pip install -e .

CMD ["python3", "-u", "src/youtooler.py", "--url", ""]
