# syntax=docker/dockerfile:1

# FROM python:3.9

# FROM nvidia/cuda:11.1.1-devel-ubuntu20.04

FROM rocm/pytorch

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update

RUN apt-get install -y python3-setuptools

RUN apt-get install -y python3-pip

RUN apt-get install -y python3-dev

RUN apt-get install -y python3-venv

RUN apt-get install -y git

RUN apt-get install -y ffmpeg

RUN pip3 install git+https://github.com/abdeladim-s/subsai.git@4cfbda07aad112057304e145d1f11023f3a892c2

RUN apt-get clean

RUN rm -rf /var/lib/apt/lists/*

EXPOSE 9091-9100

ENV PORT=9091

COPY . .

RUN pip3 install -r requirements.txt

WORKDIR backend/node/

CMD python3 -u worker_accelerated.py $PORT