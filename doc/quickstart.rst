==========
Quickstart
==========

------------
Introduction
------------

This is a Python module to interface with the JScrambler javascript
transformation service.  The Python module offers a trivally simple
API to transform you javacsript and html files.

------------
Installation
------------

This module has been tested to work in both Python 2.7 and 3.4.  The
only non-standard Python dependency is the ``requests`` module.

To install jscrambler, simply install the ``jscrambler`` package from PyPI.  You can use, pip, for instance::

  $ pip install jscrambler

------------
Credentials
------------

To use jscrambler, you need to subscribe to the server and obtain
access credentials to use the server.  Get your API credentials at
https://jscrambler.com/en/account/api_access.  There you will see two
values, *Access key* and *Secret key*, which allow you to submit
projects.

------------------
Configuration file
------------------

It is easier if you create a json configuration file, such as this one (let's call it ``config.json``):

.. code-block:: javascript

 {
     // acess credentials, replace with your own
     "keys": {
         "accessKey": "YOUR_ACCESS_KEY",
         "secretKey": "YOUR_SECRET_KEY"
     },

     // where to find the source .js files
     "filesSrc": ["lib/**/*.js"],

     // directory where to place the modified files
     "filesDest": "build/",

     // parameters that control the transformations available
     "params": {
         "function_outlining": "true",
         "rename_all": "true"
     }
 }


-------------------
Minimal python code
-------------------

Here's some sample python code to process some files, assuming that the output
build directory is already created:

.. code-block:: python

    import jscrambler
    import json

    # reads the json configuration file
    with open("config.json", "rt") as jsonfile:
        config = json.load(jsonfile)

    # creates a jscrambler client context
    client = jscrambler.Client(config["keys"]["accessKey"],
                               config["keys"]["secretKey"])

    # processes the files specified in the configuration
    client.process(config)

.. _django:

------------------
Django integration
------------------

Although jscrambler can be integrated with any web framework in any
programming language, the jscrambler python package comes with some
support for Django projects out of the box.

If you have a Django project that uses the standard
``django.contrib.staticfiles`` application to support static files, then you
already know about the ``STATIC_ROOT`` django setting.  This setting contains
the path of a directory to which all the static files will be collected.  This
is triggered by running the command ``python manage.py collectstatic`` when you
want to deploy new static files into an HTTP server, such as nginx or apache
httpd.

To add jscrambler into the workflow, you begin by adding the djcrambler
configuration to the Django project settings (`myproject`/``settings.py``)::

    JSCRAMBLER_CONFIG = { my config }

The ``JSCRAMBLER_CONFIG`` setting has to contain dict based structure
with the usual jscrambler configuration parameters.  If you wish, you
can easily load it from an external JSON file, thus::

    import json
    with open("config.json", "r") as configfile:
        JSCRAMBLER_CONFIG = json.load(configfile)

Another change in the Django settings that you need is to add ``jscrambler`` to
the ``INSTALLED_APPS``::

 INSTALLED_APPS = (
    'django.contrib.staticfiles',
    #...
    'jscrambler', # <--- add this app to your project
 )

After these changes, you will get a new Django management command
called ``scramblestatic``.  This command, which should run after
``collectstatic``, takes all files matching any of the ``filesSrc``
patterns from the config, relative to ``STATIC_ROOT``, and replace
them in-place with the scrambled versions::

  $ python manage.py collectstatic
  $ python manage.py scramblestatic

.. note::

  if the config parameter ``filesSrc`` is missing, it defaults to
  ``**/*.js`` and ``**/*.html``, which matches all Javascript and HTML
  files found under ``STATIC_ROOT``.

There is no out-of-the-box support for processing Django templates yet, so you
should make sure to write your valuable Javascript code that you wish to protect
as clearly separated static files, instead of placing it inside Django
templates.

.. warning::

  If you have a setup in which the HTTP server is serving static files
  directly from ``STATIC_ROOT``, then running the commands
  ``collectstatic`` and ``scramblestatic`` while the HTTP server is
  running will temporarily expose your original sources to the
  Internet.  Therefore, it is recommanded that your ``STATIC_ROOT``
  points to a temporary directory, which replaces the live one only
  after the ``scramblestatic`` command is finished.
