import pytest
import os
import codecs
import jscrambler.rest
from httmock import HTTMock, response, urlmatch


TEST_ACCESS_KEY = "1234567435344324213123123232323215652211"
TEST_SECRET_KEY = "8799834787827382382657637642847823734212"
TEST_FILE1 = os.path.relpath(os.path.join(os.path.dirname(__file__),
                             "test1.js"))


@pytest.mark.parametrize("file_obj_mode", [False, True])
def test_post(file_obj_mode):
    url = "http://api.jscrambler.com/v3"
    access_key = codecs.decode(TEST_ACCESS_KEY.encode("ascii"), "hex_codec")
    secret_key = codecs.decode(TEST_SECRET_KEY.encode("ascii"), "hex_codec")

    # list of (param_name, file_name, file_contents)
    files_received = []
    params_received = []

    @urlmatch(method='POST', path=r'/v3/code\.json')
    def jscrambler_server_mock(_url, request):
        files = request.original.files
        for param_name, (file_name, file_obj) in files.items():
            file_obj.seek(0)
            file_contents = file_obj.read().decode("ascii")
            files_received.append((param_name,
                                   file_name,
                                   file_contents))
        params_received.append(request.original.data)
        headers = {'content-type': 'application/json'}
        content = {'id': '123'}
        return response(200, content, headers, request=request)

    with HTTMock(jscrambler_server_mock):
        if file_obj_mode:
            with open(TEST_FILE1, "rb") as file_obj:
                resp = jscrambler.rest.post(
                    url, access_key, secret_key,
                    [(TEST_FILE1, file_obj)],
                    foo="bar", zbr="xpto")
        else:
            resp = jscrambler.rest.post(url, access_key, secret_key,
                                        [TEST_FILE1],
                                        foo="bar", zbr="xpto")

    assert resp == {'id': '123'}
    assert files_received == [('file_0', 'tests/test1.js', 'hello()\n')]
    params = dict(params_received[0])
    assert params.get('foo') == 'bar'
    assert params.get('zbr') == 'xpto'


def test_status():
    url = "http://api.jscrambler.com/v3"
    access_key = codecs.decode(TEST_ACCESS_KEY.encode("ascii"), "hex_codec")
    secret_key = codecs.decode(TEST_SECRET_KEY.encode("ascii"), "hex_codec")

    params_received = []

    @urlmatch(method='GET', path=r'/v3/code\.json')
    def jscrambler_server_mock(_url, request):
        params = request.original.params
        params_received.append(params)
        if params.get('status') == "123":
            content = {'id': '123'}
        elif params.get('status') is None:
            content = b'[{"id": "123"}]'
        else:
            return
        headers = {'content-type': 'application/json'}
        return response(200, content, headers, request=request)

    with HTTMock(jscrambler_server_mock):
        params_received = []
        resp1 = jscrambler.rest.get_status(url, access_key, secret_key,
                                           "123", foo="bar", offset=0, limit=0)
        params = dict(params_received[0])
        assert params.get('foo') == 'bar'
        params_received = []
        resp2 = jscrambler.rest.get_status(url, access_key, secret_key)

    assert resp1 == {'id': '123'}
    assert resp2 == [{'id': '123'}]


def test_project_status():
    url = "http://api.jscrambler.com/v3"
    access_key = codecs.decode(TEST_ACCESS_KEY.encode("ascii"), "hex_codec")
    secret_key = codecs.decode(TEST_SECRET_KEY.encode("ascii"), "hex_codec")

    params_received = []

    @urlmatch(method='GET', path=r'/v3/code/123\.json')
    def jscrambler_server_mock(_url, request):
        params = request.original.params
        params_received.append(params)
        content = b'{"id": "123"}'
        headers = {'content-type': 'application/json'}
        return response(200, content, headers, request=request)

    with HTTMock(jscrambler_server_mock):
        resp1 = jscrambler.rest.get_project_status(url,
                                                   access_key,
                                                   secret_key,
                                                   "123",
                                                   foo="bar",
                                                   symbol_table="abc")
    params = dict(params_received[0])
    assert params.get('foo') == 'bar'
    assert resp1 == {'id': '123'}


@pytest.mark.parametrize("return_error", [False, True])
def test_project_zip(return_error):
    url = "http://api.jscrambler.com/v3"
    access_key = codecs.decode(TEST_ACCESS_KEY.encode("ascii"), "hex_codec")
    secret_key = codecs.decode(TEST_SECRET_KEY.encode("ascii"), "hex_codec")

    params_received = []

    @urlmatch(method='GET', path=r'/v3/code/123\.zip')
    def jscrambler_server_mock(_url, request):
        params = request.original.params
        params_received.append(params)
        content = b'zipcontent'
        headers = {'content-type': 'application/zip'}
        return response(400 if return_error else 200,
                        content, headers, request=request)

    with HTTMock(jscrambler_server_mock):
        if return_error:
            with pytest.raises(RuntimeError):
                jscrambler.rest.get_project_zip(url,
                                                access_key,
                                                secret_key,
                                                "123")
        else:
            resp1 = jscrambler.rest.get_project_zip(url,
                                                    access_key,
                                                    secret_key,
                                                    "123")
            assert resp1 == b'zipcontent'


def test_project_source_info():
    url = "http://api.jscrambler.com/v3"
    access_key = codecs.decode(TEST_ACCESS_KEY.encode("ascii"), "hex_codec")
    secret_key = codecs.decode(TEST_SECRET_KEY.encode("ascii"), "hex_codec")

    params_received = []

    @urlmatch(method='GET', path=r'/v3/code/123/a3b85573d493d803537555f48a1a7ac9778ec19f\.json')
    def jscrambler_server_mock(_url, request):
        params = request.original.params
        params_received.append(params)
        content = b'{"foo": "bar"}'
        headers = {'content-type': 'application/json'}
        return response(200, content, headers, request=request)

    with HTTMock(jscrambler_server_mock):
        resp1 = jscrambler.rest.get_project_source_info(
            url,
            access_key,
            secret_key,
            "123",
            "a3b85573d493d803537555f48a1a7ac9778ec19f")

    assert resp1 == {"foo": "bar"}


def test_get_project_source():
    url = "http://api.jscrambler.com/v3"
    access_key = codecs.decode(TEST_ACCESS_KEY.encode("ascii"), "hex_codec")
    secret_key = codecs.decode(TEST_SECRET_KEY.encode("ascii"), "hex_codec")

    params_received = []

    @urlmatch(method='GET', path=r'/v3/code/123/a3b85573d493d803537555f48a1a7ac9778ec19f\.js')
    def jscrambler_server_mock(_url, request):
        params = request.original.params
        params_received.append(params)
        content = b'foo = bar'
        headers = {}
        return response(200, content, headers, request=request)

    with HTTMock(jscrambler_server_mock):
        resp1 = jscrambler.rest.get_project_source(
            url,
            access_key,
            secret_key,
            "123",
            "a3b85573d493d803537555f48a1a7ac9778ec19f",
            "js")

    assert resp1 == "foo = bar"


def test_delete_project():
    url = "http://api.jscrambler.com/v3"
    access_key = codecs.decode(TEST_ACCESS_KEY.encode("ascii"), "hex_codec")
    secret_key = codecs.decode(TEST_SECRET_KEY.encode("ascii"), "hex_codec")

    params_received = []

    @urlmatch(method='DELETE', path=r'/v3/code/123.json')
    def jscrambler_server_mock(_url, request):
        params = request.original.params
        params_received.append(params)
        content = {'id': '123', 'deleted': True}
        headers = {'content-type': 'application/json'}
        return response(200, content, headers, request=request)

    with HTTMock(jscrambler_server_mock):
        resp1 = jscrambler.rest.delete_project(
            url,
            access_key,
            secret_key,
            "123")

    assert resp1 == {'id': '123', 'deleted': True}
