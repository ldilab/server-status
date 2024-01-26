# syntax=docker/dockerfile:1

FROM python:3.10-alpine

RUN apk add build-base linux-headers
RUN apk add --no-cache gcc

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]