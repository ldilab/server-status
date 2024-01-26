# syntax=docker/dockerfile:1

FROM python:3.10-alpine

RUN apk add build-base linux-headers
RUN apk add --no-cache gcc

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "src/app.py" ]
