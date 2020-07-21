from glob import glob
import os

import pkg_resources

from .__about__ import __version__


config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 24|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-notes:{{ NOTES_VERSION }}",
        "HOST": "notes.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "notes",
        "MYSQL_USERNAME": "notes",
    },
}

templates = pkg_resources.resource_filename("tutornotes", "templates")
hooks = {
    "init": ["mysql", "lms", "notes"],
    "build-image": {"notes": "{{ NOTES_DOCKER_IMAGE }}"},
    "remote-image": {"notes": "{{ NOTES_DOCKER_IMAGE }}"},
}


def patches():
    all_patches = {}
    for path in glob(
        os.path.join(pkg_resources.resource_filename("tutornotes", "patches"), "*")
    ):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
