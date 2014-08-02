=============
Configuration
=============

This section describes the recommended configuration format for use
with the jscrambler API.  The recommendation is to use JSON format,
but essencially the API can use just dict-based structures that can be
either obtained by parsing a JSON configuration file or constructed
programatically.

#########################
Configuration File Format
#########################

The snippet below illustrates an example configuration file

.. code-block:: javascript

	{
	  "filesSrc": [""],
	  "filesDest": "dist/",
	  "host": "api.jscrambler.com", // default
	  "port": 443, // default
	  "apiVersion": 3, // default
	  "keys": {
	    "accessKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
	    "secretKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
	  },
	  "params": {
	    "string_splitting": "%DEFAULT%",
	    "function_reorder": "%DEFAULT%",
	    "function_outlining": "%DEFAULT%",
	    "dot_notation_elimination": "%DEFAULT%",
	    "expiration_date": "2199-01-01",
	    "rename_local": "%DEFAULT%",
	    "whitespace": "%DEFAULT%",
	    "literal_duplicates": "%DEFAULT%"
	  },
	  "deleteProject": false // default
	}


All entries marked with *%DEFAULT%* can be omitted and the client should assume those values.
All entries in the "params" section are also optional. The above example only shows a subset of the existing parameters. For a complete listing of possible parameters, please check here:
`Optional parameters`_ (though this knowledge shouldn't impact anything on the client implementation).

.. _filesSrc:

filesSrc
--------
This configuration entry is a *list of paths* to files that should be included in the project. By *project* we don't mean all the files pertaining to the web application, but only the files that JScrambler needs to transform. Right now this is limited to ``*.htm(l)`` and ``*.js`` files.  Globbing patterns are supported, for example:
  - :literal:`["lib/**/*.js"]` should resolve to all JS files inside the lib folder and all the children folders
  - :literal:`["lib/**"]` should resolve to all files inside the lib folder and all the children folders
  - :literal:`["lib/*.js"]` should resolve to all JS files directly inside the ``lib`` folder

Params
------
For a complete listing of possible parameters, see `Optional parameters`_.


.. _Optional parameters: https://jscrambler.com/en/help/webapi/documentation#optional_parameters

##############################
Configuration usage in the API
##############################

The configuration is used as follows in the client API:

 - In the :class:`jscrambler.Client` constructor, the configuration is not read
   directly but all the constructor parameters (``accessKey``,
   ``secretKey``, ``host``, ``port``, and ``apiVersion``), can be
   taken directly from the configuration file;
 - The :meth:`jscrambler.Client.process` convenience method takes a
   configuration file as parameter; the ``params`` section of the
   configuration file is used directly in the upload request, and the
   ``filesSrc`` and ``filesDest`` configuration options are used to
   find the files to upload and the directory where to download the
   transformed versions, respectively;
 - The ``filesSrc`` parameter is honored by the ``scramblestatic``
   Django management command, see :ref:`django`.
