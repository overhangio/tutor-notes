# syntax=docker/dockerfile:1.4
FROM docker.io/python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && \
  apt upgrade -y && \
  apt install -y \
    locales \
    git \
    python3-dev \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config && \
  sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
  locale-gen
ENV LC_ALL en_US.UTF-8

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
RUN --mount=type=cache,target=/app/.cache/pip,sharing=shared pip install setuptools==69.2.0 pip==24.0 wheel==0.43.0
RUN --mount=type=cache,target=/app/.cache/pip,sharing=shared pip install -r requirements/base.txt

EXPOSE 8000
CMD gunicorn --workers=2 --name notes --bind=0.0.0.0:8000 --max-requests=1000 notesserver.wsgi:application
