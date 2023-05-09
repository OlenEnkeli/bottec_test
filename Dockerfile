FROM python:3.11 AS bottec_test

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
