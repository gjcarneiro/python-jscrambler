# Copyright (c) 2013-2014 Gustavo J. A. M. Carneiro <gjcarneiro@gmail.com>

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Adapted by JScrambler - 2013

from __future__ import print_function
import os
import json

import jscrambler


def test():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)

    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)

    # If there exists a config.json.local, merge it in
    if os.path.exists("config.json.local"):
        with open("config.json.local", "r") as jsonfile:
            config.update(json.load(jsonfile))

    client = jscrambler.Client(config["keys"]["accessKey"],
                               config["keys"]["secretKey"])

    print("pyjscrambler 1.0")
    print("Using API URL: {}".format(client.api_url))

    try:
        os.mkdir("build")
    except OSError:
        pass

    if 1:
        result = client.upload_code(config["filesSrc"], **config["params"])
        project_id = result['id']
        client.poll_project(project_id)
        client.download_code(project_id, config['filesDest'])
    else:
        client.process(config)


if __name__ == '__main__':
    test()
