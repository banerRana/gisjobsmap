from unittest import mock, TestCase
import requests
from scraper.api import DataAPI
from .mock_responses import *


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://someurl.com/test.json':
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
        return MockResponse({"key2": "value2"}, 200)
    return MockResponse(None, 404)


class TestApi(TestCase):
    pass
    # @mock.patch('scraper.api.DataAPI')
    # def test_init(self):
    #     api = DataAPI()

    # def test_set_inactive(self, fake_get):
    #     fake_get.return_value.status_code = 200
    #     fake_get.return_value.json.return_value = set_inactive_response
    #     pass
