FROM python:3.12-alpine
LABEL maintainer="judviiioff@gmail.com"
RUN apk add --no-cache bash
WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
