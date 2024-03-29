# syntax=docker/dockerfile:1.4
FROM docker.io/ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && \
  apt upgrade -y && \
  apt install -y \
    language-pack-en \
    git \
    python3 \
    python3-pip \
    python3-venv \
    libmysqlclient-dev \
    pkg-config
RUN ln -s /usr/bin/python3 /usr/bin/python

###### Git-clone Notes repo ######
ARG APP_USER_ID=1000
RUN useradd --home-dir /app --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

RUN git clone {{ NOTES_REPOSITORY }} --branch {{ NOTES_REPOSITORY_VERSION }} --depth 1 /app/edx-notes-api
WORKDIR /app/edx-notes-api

###### Install python venv ######
RUN python -m venv /app/venv
ENV PATH /app/venv/bin:${PATH}
# https://pypi.org/project/setuptools/
# https://pypi.org/project/pip/
# https://pypi.org/project/wheel/
RUN --mount=type=cache,target=/app/.cache/pip,sharing=shared pip install setuptools==68.2.2 pip==23.2.1 wheel==0.41.2
RUN --mount=type=cache,target=/app/.cache/pip,sharing=shared pip install -r requirements/base.txt

EXPOSE 8000
CMD gunicorn --workers=2 --name notes --bind=0.0.0.0:8000 --max-requests=1000 notesserver.wsgi:application
