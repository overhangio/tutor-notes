from .common import *

SECRET_KEY = "{{ NOTES_SECRET_KEY }}"
ALLOWED_HOSTS = [
    "notes",
    "{{ NOTES_HOST }}",
    "{{ NOTES_HOST }}:8120",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": {{ MYSQL_PORT }},
        "NAME": "{{ NOTES_MYSQL_DATABASE }}",
        "USER": "{{ NOTES_MYSQL_USERNAME }}",
        "PASSWORD": "{{ NOTES_MYSQL_PASSWORD }}",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

CLIENT_ID = "notes"
CLIENT_SECRET = "{{ NOTES_OAUTH2_SECRET }}"

# Meilisearch credentials
ES_DISABLED = True
MEILISEARCH_ENABLED = True
MEILISEARCH_URL = "{{ MEILISEARCH_URL }}"
MEILISEARCH_API_KEY = "{{ MEILISEARCH_API_KEY }}"
MEILISEARCH_INDEX = "{{ MEILISEARCH_INDEX_PREFIX }}student_notes"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

{{ patch("notes-settings") }}
