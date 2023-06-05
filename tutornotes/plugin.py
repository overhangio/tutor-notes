from __future__ import annotations

from glob import glob
import os
import typing as t

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
        "REPOSITORY": "https://github.com/openedx/edx-notes-api",
        "REPOSITORY_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
    },
}

# Initialization hooks

# To add a custom initialization task, create a bash script template under:
# tutorcodejail/templates/codejail/tasks/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    ("mysql", ("notes", "tasks", "mysql", "init")),
    ("lms", ("notes", "tasks", "lms", "init")),
    ("notes", ("notes", "tasks", "notes", "init")),
]

# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutornotes", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))

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

@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_edx_notes_api(volumes, name):
    """
    When mounting edx-notes-api with `--mount=/path/to/edx-notes-api`,
    bind-mount the host repo in the notes container.
    """
    if name == "edx-notes-api":
        path = "/app/edx-notes-api"
        volumes += [
            ("notes", path),
            ("notes-job", path),
        ]
    return volumes

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
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
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
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)

# Notes public hosts
@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _notes_public_hosts(hosts: list[str], context_name: t.Literal["local", "dev"]) -> list[str]:
    if context_name == "dev":
        hosts += ["{{ NOTES_HOST }}:8120"]
    else:
        hosts += ["{{ NOTES_HOST }}"]
    return hosts
