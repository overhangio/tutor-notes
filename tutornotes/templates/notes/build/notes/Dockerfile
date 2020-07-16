FROM docker.io/ubuntu:20.04
MAINTAINER Overhang.io <contact@overhang.io>

RUN apt update && \
  apt upgrade -y && \
  # python 3.8
  apt install -y language-pack-en git python3 python3-pip libmysqlclient-dev
RUN ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip


RUN mkdir /openedx
RUN git clone https://github.com/edx/edx-notes-api --branch open-release/juniper.2 --depth 1 /openedx/edx-notes-api
WORKDIR /openedx/edx-notes-api

RUN pip3 install -r requirements/base.txt

EXPOSE 8000
CMD gunicorn --workers=2 --name notes --bind=0.0.0.0:8000 --max-requests=1000 notesserver.wsgi:application
