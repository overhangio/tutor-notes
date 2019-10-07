from .common import *

SECRET_KEY = "{{ NOTES_SECRET_KEY }}"
ALLOWED_HOSTS = [
    "localhost",
    "notes",
    "notes.localhost",
    "{{ NOTES_HOST }}",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": {{MYSQL_PORT}},
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

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "notesserver.highlight.ElasticsearchSearchEngine",
        "URL": "http://{{ ELASTICSEARCH_HOST }}:{{ ELASTICSEARCH_PORT }}/",
        "INDEX_NAME": "notes",
    }
}

LOGGING["handlers"]["local"] = LOGGING["handlers"]["console"].copy()
