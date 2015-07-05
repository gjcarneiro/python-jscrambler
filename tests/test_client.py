from __future__ import unicode_literals
import os
import codecs
from jscrambler import Client
from zipfile import ZipFile
import pytest
import datetime


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


@pytest.mark.parametrize("numtries,error_id", [
    (3, '0'),
    (3, '1'),
    (12, '0'),
])
def test_poll_project(monkeypatch, numtries, error_id):

    calls_made = []
    nonlocals = [numtries]

    def get_project_status(api_url, access_key, secret_key, project_id,
                           symbol_table=None, **opt_params):

        calls_made.append((api_url, access_key, secret_key, project_id,
                           symbol_table, opt_params))

        # python 2 missing nonlocal support
        count = nonlocals[0]
        count -= 1
        nonlocals[0] = count

        status = {"id": project_id, 'error_id': error_id}

        if count <= 0:
            status['finished_at'] = datetime.datetime.now().isoformat()
        else:
            status['finished_at'] = None

        return status

    import jscrambler.rest
    monkeypatch.setattr(jscrambler.rest,
                        "get_project_status",
                        get_project_status)

    client = Client(TEST_ACCESS_KEY, TEST_SECRET_KEY)
    if numtries > 10 or error_id != '0':
        with pytest.raises(RuntimeError):
            client.poll_project(123, poll_pause=0.01, maximum_poll_retries=10)
    else:
        retval = client.poll_project(123, poll_pause=0.01,
                                     maximum_poll_retries=10)

        assert retval.get('id') == 123
        assert retval.get('error_id') == '0'
        assert 'finished_at' in retval


def test_download_project(monkeypatch, tmpdir):
    tmpdir = str(tmpdir)
    get_project_zip_calls = []

    def get_project_zip(api_url, access_key, secret_key, project_id,
                        **opt_params):
        get_project_zip_calls.append((api_url, access_key, secret_key,
                                      project_id, opt_params))
        if project_id == 123:
            try:
                from io import BytesIO
            except ImportError:
                from StringIO import StringIO as BytesIO
            zipbuf = BytesIO()
            with ZipFile(zipbuf, 'w') as zipfile:
                zipfile.write("tests/test1.js")
            return zipbuf.getvalue()
        else:
            return b''

    import jscrambler.rest
    monkeypatch.setattr(jscrambler.rest,
                        "get_project_zip",
                        get_project_zip)

    projects_deleted = []

    def delete_project(api_url, access_key, secret_key, project_id,
                       **opt_params):
        projects_deleted.append(project_id)

    monkeypatch.setattr(jscrambler.rest,
                        "delete_project",
                        delete_project)

    client = Client(TEST_ACCESS_KEY, TEST_SECRET_KEY)
    client.download_code(123, tmpdir)
    assert os.path.exists(os.path.join(tmpdir, "tests", "test1.js"))
    assert projects_deleted == [123]


@pytest.mark.parametrize("config", [
    {"filesSrc": ["somefiles"],
     "params": {"option1": "value1"},
     "filesDest": "destdir"},
    "tests/test_config.json",
])
def test_process(monkeypatch, config):
    upload_calls = []
    poll_calls = []
    download_calls = []

    def upload(*args, **kwargs):
        upload_calls.append((args, kwargs))
        return {"id": 123}

    def poll_project(*args, **kwargs):
        poll_calls.append((args, kwargs))

    def download_code(*args, **kwargs):
        download_calls.append((args, kwargs))

    client = Client(TEST_ACCESS_KEY, TEST_SECRET_KEY)

    monkeypatch.setattr(client, "upload_code", upload)
    monkeypatch.setattr(client, "poll_project", poll_project)
    monkeypatch.setattr(client, "download_code", download_code)

    client.process(config)
    assert upload_calls == [((['somefiles'],), {'option1': 'value1'})]
    assert poll_calls == [((123,), {})]
    assert download_calls == [((123, 'destdir'), {})]
