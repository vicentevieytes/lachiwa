FROM python:3.12-slim

WORKDIR /usr/src/app

COPY lachiwa/requirements.txt .

RUN pip install -r requirements.txt

COPY lachiwa/ .

EXPOSE 5000
