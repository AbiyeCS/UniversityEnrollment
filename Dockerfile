FROM python:3.9-slim-buster

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y netcat
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app

CMD python manage.py migrate