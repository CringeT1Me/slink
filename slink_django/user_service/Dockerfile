FROM python:3.12-slim

WORKDIR /user_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000