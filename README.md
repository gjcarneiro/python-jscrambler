python-jscrambler 2.0
----------------

Apart from the modules which are normally installed by default with Python,
you may have to install the following:
- requests

If you have easy_install in the system, all you have to do is:
easy_install requests

To use python-jscrambler, you only have to edit the configuration in config.json.
You have to:
- Insert your access_key and secret_key;
- List the target files (HTML and JS only), or a zip file
  note: pointing to a directory is not yet supported;
- Choose the source code transformations you want to use.
  Check https://jscrambler.com/en/help/webapi/ to know which ones are available.

Any questions, please contact JScrambler Support - support@jscrambler.com

[![Build Status](https://travis-ci.org/gjcarneiro/python-jscrambler.svg?branch=master)](https://travis-ci.org/gjcarneiro/python-jscrambler)
