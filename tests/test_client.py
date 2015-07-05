from __future__ import unicode_literals
import codecs
from jscrambler import Client
from zipfile import ZipFile
import pytest


TEST_ACCESS_KEY = "1234567435344324213123123232323215652211"
TEST_SECRET_KEY = "8799834787827382382657637642847823734212"

TEST_ACCESS_KEY_BIN = codecs.decode(TEST_ACCESS_KEY.encode("ascii"),
                                    "hex_codec")
TEST_SECRET_KEY_BIN = codecs.decode(TEST_SECRET_KEY.encode("ascii"),
                                    "hex_codec")


def test_client_default():
    client1 = Client(TEST_ACCESS_KEY, TEST_SECRET_KEY)
    assert client1.api_url == 'https://api.jscrambler.com/v3'
    ak = codecs.encode(client1.access_key, "hex_codec").decode("ascii")
    sk = codecs.encode(client1.secret_key, "hex_codec").decode("ascii")
    assert ak == TEST_ACCESS_KEY
    assert sk == TEST_SECRET_KEY


def test_client_init_params():
    client1 = Client(TEST_ACCESS_KEY, TEST_SECRET_KEY,
                     host="foo.com",
                     port=8080,
                     apiVersion=123)
    assert client1.api_url == 'http://foo.com:8080/v123'


@pytest.mark.parametrize("files_src", [
    ["tests/test1.js"],
    "tests/test1.js",
])
def test_upload_code(monkeypatch, files_src):
    post_calls = []

    def post(api_url, access_key, secret_key, files, **opt_params):
        post_calls.append((api_url, access_key, secret_key, files, opt_params))
        return {"this_is_a_json": "response"}

    import jscrambler.rest
    monkeypatch.setattr(jscrambler.rest, "post", post)

    client = Client(TEST_ACCESS_KEY, TEST_SECRET_KEY)
    retval = client.upload_code(files_src, foo="bar")

    assert retval == {"this_is_a_json": "response"}
    assert len(post_calls) == 1
    post_call = post_calls[0]

    assert post_call[:3] == ('https://api.jscrambler.com/v3',
                             TEST_ACCESS_KEY_BIN,
                             TEST_SECRET_KEY_BIN,
                             )
    assert post_call[4] == dict(foo="bar")
    post_files = post_call[3]
    assert len(post_files) == 1
    assert post_files[0][0] == "project.zip"
    file_mem = post_files[0][1]

    zipfile = ZipFile(file_mem, "r")
    assert zipfile.namelist() == ['tests/test1.js']
    source = zipfile.open("tests/test1.js", "r").read()
    assert source == b'hello()\n'


def test_get_info(monkeypatch):

    calls_made = []

    def get_status(api_url, access_key, secret_key, status=None, offset=None,
                   limit=None, **opt_params):
        calls_made.append((api_url, access_key, secret_key,
                           status, offset,
                           limit, opt_params))
        return {"this_is_a_json": "response"}

    import jscrambler.rest
    monkeypatch.setattr(jscrambler.rest, "get_status", get_status)

    client = Client(TEST_ACCESS_KEY, TEST_SECRET_KEY)
    retval = client.get_info()

    assert retval == {"this_is_a_json": "response"}
    assert calls_made == [('https://api.jscrambler.com/v3',
                           TEST_ACCESS_KEY_BIN,
                           TEST_SECRET_KEY_BIN,
                           None, None, None, {})]


def test_get_project_info(monkeypatch):

    calls_made = []

    def get_project_status(api_url, access_key, secret_key, project_id,
                           symbol_table=None, **opt_params):
        calls_made.append((api_url, access_key, secret_key, project_id,
                           symbol_table, opt_params))
        return {"this_is_a_json": "response"}

    import jscrambler.rest
    monkeypatch.setattr(jscrambler.rest,
                        "get_project_status",
                        get_project_status)

    client = Client(TEST_ACCESS_KEY, TEST_SECRET_KEY)
    retval = client.get_info(123)

    assert retval == {"this_is_a_json": "response"}
    assert calls_made == [('https://api.jscrambler.com/v3',
                           TEST_ACCESS_KEY_BIN,
                           TEST_SECRET_KEY_BIN,
                           123,
                           None,
                           {})]
