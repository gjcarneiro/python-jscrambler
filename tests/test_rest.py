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

        @urlmatch(path=r'/v3/code\.json')
        def jscrambler_server_mock(url, request):
            files = request.original.files
            for param_name, (file_name, file_obj) in files.items():
                file_obj.seek(0)
                file_contents = file_obj.read().decode("ascii")
                files_received.append((param_name,
                                       file_name,
                                       file_contents))

            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            content = {'id': '123'}
            return response(200, content, headers, request=request)

        with HTTMock(jscrambler_server_mock):
            resp = jscrambler.rest.post(url, access_key, secret_key,
                                        [TEST_FILE1])

        self.assertEqual(resp, {'id': '123'})
        self.assertEqual(files_received, [('file_0', 'tests/test1.js', 'hello()\n')])

if __name__ == '__main__':
    unittest.main()
