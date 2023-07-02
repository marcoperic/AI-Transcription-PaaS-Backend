# syntax=docker/dockerfile:1

FROM python:3.9

RUN apt-get update

RUN apt-get install -y python3-setuptools

RUN apt-get install -y python3-pip

RUN apt-get install -y python3-dev

RUN apt-get install -y python3-venv

RUN apt-get install -y git

RUN apt-get install -y ffmpeg

RUN apt-get clean

RUN rm -rf /var/lib/apt/lists/*

EXPOSE 9091-9100

COPY . .

ENV PORT=9091

RUN pip3 install git+https://github.com/abdeladim-s/subsai.git@936aa4fc2093ef1232449012df5b884b54e1f5b6

RUN pip3 install -r requirements.txt

WORKDIR backend/node/

CMD python3 -u worker.py $PORT