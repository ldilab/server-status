# syntax=docker/dockerfile:1

FROM nvcr.io/nvidia/cuda:11.0.3-base-ubuntu20.04

# RUN apk add build-base linux-headers

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
