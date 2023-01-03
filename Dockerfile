FROM python:3.9-alpine3.13
LABEL maintainer="pyrack.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

WORKDIR /app
EXPOSE 8000

RUN pip install -r /requirements.txt