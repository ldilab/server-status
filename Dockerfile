# syntax=docker/dockerfile:1

FROM python:3.10-alpine

RUN apk add build-base linux-headers
RUN apk --update add --no-cache nvidia-utils

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
