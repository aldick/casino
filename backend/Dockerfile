FROM python:3.12-alpine

RUN apk update && \
	apk add nano

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /casino

COPY requirements.txt /casino
RUN pip install --no-cache-dir -r requirements.txt

COPY . /casino