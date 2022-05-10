from glob import glob
import os

import pkg_resources

from tutor import hooks as tutor_hooks

from .__about__ import __version__


config = {
    "unique": {
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

# Initialization hooks
tutor_hooks.Filters.COMMANDS_INIT.add_item((
    "mysql",
    ("notes", "tasks", "mysql", "init"),
))
tutor_hooks.Filters.COMMANDS_INIT.add_item((
    "lms",
    ("notes", "tasks", "lms", "init"),
))
tutor_hooks.Filters.COMMANDS_INIT.add_item((
    "notes",
    ("notes", "tasks", "notes", "init"),
))

# Image management
tutor_hooks.Filters.IMAGES_BUILD.add_item((
    "notes",
    ("plugins", "notes", "build", "notes"),
    "{{ NOTES_DOCKER_IMAGE }}",
    (),
))
tutor_hooks.Filters.IMAGES_PULL.add_item((
    "notes",
    "{{ NOTES_DOCKER_IMAGE }}",
))
tutor_hooks.Filters.IMAGES_PUSH.add_item((
    "notes",
    "{{ NOTES_DOCKER_IMAGE }}",
))

####### Boilerplate code
# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutornotes", "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("notes/build", "plugins"),
        ("notes/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutornotes", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"NOTES_{key}", value)
        for key, value in config.get("defaults", {}).items()
    ]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"NOTES_{key}", value)
        for key, value in config.get("unique", {}).items()
    ]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))
