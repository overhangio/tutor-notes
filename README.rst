Students notes plugin for `Tutor <https://docs.tutor.edly.io>`_
===================================================================

This is a plugin for `Tutor <https://docs.tutor.edly.io>`_ to easily add the `Open edX note-taking app <https://github.com/openedx/edx-notes-api>`_ to an Open edX platform. This app allows students to annotate portions of the courseware (see `the official documentation <https://docs.openedx.org/en/latest/educators/how-tos/course_development/exercise_tools/enable_notes.html>`_).

.. image:: https://docs.openedx.org/en/latest/_images/SFD_SN_bodyexample.png
    :alt: Notes in action

Installation
------------

The plugin is currently bundled with the `binary releases of Tutor <https://github.com/overhangio/tutor/releases>`_. If you have installed Tutor from source, you will have to install this plugin from source, too::

    tutor plugins install notes

Then, to enable this plugin, run::

    tutor plugins enable notes

Then, to make migrations & tasks::

    tutor local launch

You should beware that the ``notes.<LMS_HOST>`` domain name should exist and point to your server. For instance, if your LMS is hosted at http://myopenedx.com, the notes service should be found at http://notes.myopenedx.com.

If you would like to host the notes service at a different domain name, you can set the ``NOTES_HOST`` configuration variable (see below). When testing Tutor on a local computer, this will be automatically set to notes.local.openedx.io.

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
- ``NOTES_REPOSITORY`` (default: ``"https://github.com/openedx/edx-notes-api"``)
- ``NOTES_REPOSITORY_VERSION`` (default: ``"{{ OPENEDX_COMMON_VERSION }}"``)

These values can be modified with ``tutor config save --set PARAM_NAME=VALUE`` commands.

Debugging
---------

To debug the notes API service, you are encouraged to mount the edx-notes-api repo from the host in the development container:

    tutor dev start --mount /path/to/edx-notes-api

Feel free to add breakpoints (``breakpoint()``) anywhere in your source code to debug your application.

Troubleshooting
---------------

This Tutor plugin is maintained by Jhony Avella from `eduNEXT <https://www.edunext.co/>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.

License
-------

This software is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor-notes/blob/release/LICENSE.txt>`_.
