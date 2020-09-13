import os
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
ADMIN_PASS = os.environ.get('ADMIN_PASSWORD')
API_HOST = os.environ.get('API_HOST')
API_PORT = os.environ.get('API_PORT')
base_url = 'http://{}:{}/api'.format(API_HOST, API_PORT)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "{}/scraper/invalid?{}".format(base_url, args[1]):
        return MockResponse({"success": True}, 200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
        return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)