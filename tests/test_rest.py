import os
import unittest
import codecs
import jscrambler.rest
from httmock import HTTMock, response, urlmatch


TEST_ACCESS_KEY = "1234567435344324213123123232323215652211"
TEST_SECRET_KEY = "8799834787827382382657637642847823734212"
TEST_FILE1 = os.path.join(os.path.dirname(__file__), "test1.js")


class TestRest(unittest.TestCase):

    def test_post(self):
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
            resp = jscrambler.rest.post(url, access_key, secret_key,
                                        [TEST_FILE1],
                                        foo="bar", zbr="xpto")

        self.assertEqual(resp, {'id': '123'})
        self.assertEqual(files_received,
                         [('file_0', 'tests/test1.js', 'hello()\n')])
        params = dict(params_received[0])
        self.assertEqual(params.get('foo'), 'bar')
        self.assertEqual(params.get('zbr'), 'xpto')

    def test_status(self):
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
            params_received.clear()
            resp1 = jscrambler.rest.get_status(url, access_key, secret_key,
                                               "123", foo="bar")
            params = dict(params_received[0])
            self.assertEqual(params.get('foo'), 'bar')
            params_received.clear()
            resp2 = jscrambler.rest.get_status(url, access_key, secret_key)

        self.assertEqual(resp1, {'id': '123'})
        self.assertEqual(resp2, [{'id': '123'}])

    def test_project_status(self):
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
                                                       foo="bar")
        params = dict(params_received[0])
        self.assertEqual(params.get('foo'), 'bar')
        self.assertEqual(resp1, {'id': '123'})

if __name__ == '__main__':
    import logging
    logging.basicConfig(level='DEBUG')
    unittest.main()
