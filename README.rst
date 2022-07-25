Students notes plugin for `Tutor <https://docs.tutor.overhang.io>`_
===================================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ to easily add the `Open edX note-taking app <https://github.com/edx/edx-notes-api>`_ to an Open edX platform. This app allows students to annotate portions of the courseware (see `the official documentation <https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/open-release-nutmeg.master/exercises_tools/notes.html>`_).

.. image:: https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/open-release-nutmeg.master/_images/SFD_SN_bodyexample.png
    :alt: Notes in action

Installation
------------

The plugin is currently bundled with the `binary releases of Tutor <https://github.com/overhangio/tutor/releases>`_. If you have installed Tutor from source, you will have to install this plugin from source, too::

    pip install tutor-notes

Then, to enable this plugin, run::

    tutor plugins enable notes

You should beware that the ``notes.<LMS_HOST>`` domain name should exist and point to your server. For instance, if your LMS is hosted at http://myopenedx.com, the notes service should be found at http://notes.myopenedx.com.

If you would like to host the notes service at a different domain name, you can set the ``NOTES_HOST`` configuration variable (see below). When testing Tutor on a local computer, this will be automatically set to notes.local.overhang.io.

To enable student notes for a specific course, you should go to the course advanced settings in the studio, and set "Enable Student Notes" to "true". Then, hit "save changes".

Configuration
-------------

- ``NOTES_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
- ``NOTES_SECRET_KEY`` (default: ``"{{ 24|random_string }}"``)
- ``NOTES_OAUTH2_SECRET`` (default: ``"{{ 24|random_string }}"``)
- ``NOTES_DOCKER_IMAGE`` (default: ``"{{ DOCKER_REGISTRY }}overhangio/openedx-notes:{{ NOTES_VERSION }}"``)
- ``NOTES_HOST`` (default: ``"notes.{{ LMS_HOST }}"``)
- ``NOTES_MYSQL_DATABASE`` (default: ``"notes"``)
- ``NOTES_MYSQL_USERNAME`` (default: ``"notes"``)

These values can be modified with ``tutor config save --set PARAM_NAME=VALUE`` commands.

Debugging
---------

To debug the notes API service, you are encouraged to mount the edx-notes-api repo from the host in the development container:

    tutor dev start --mount /path/to/edx-notes-api

Feel free to add breakpoints (``breakpoint()``) anywhere in your source code to debug your application.
