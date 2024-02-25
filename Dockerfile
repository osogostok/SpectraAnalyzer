FROM python:3.10

WORKDIR /usr/src/app

COPY ./src/spectranalizer ./

COPY requirements.txt ./

RUN pip install -r requirements.txt
