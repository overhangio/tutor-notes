FROM docker.io/ubuntu:20.04
MAINTAINER Overhang.io <contact@overhang.io>

RUN apt update && \
  apt upgrade -y && \
  # python 3.8
  apt install -y language-pack-en git python3 python3-pip python3-venv libmysqlclient-dev
RUN ln -s /usr/bin/python3 /usr/bin/python

ARG APP_USER_ID=1000
RUN useradd --home-dir /app --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

RUN git clone https://github.com/edx/edx-notes-api --branch {{ OPENEDX_COMMON_VERSION }} --depth 1 /app/edx-notes-api
WORKDIR /app/edx-notes-api

RUN python -m venv /app/venv
ENV PATH /app/venv/bin:${PATH}
RUN pip install setuptools==44.1.0 pip==20.3.4 wheel==0.37.0
RUN pip3 install -r requirements/base.txt

EXPOSE 8000
CMD gunicorn --workers=2 --name notes --bind=0.0.0.0:8000 --max-requests=1000 notesserver.wsgi:application
