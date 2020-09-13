import json
import unittest
from tests.base import BaseTestCase


class TestGeonamesApi(BaseTestCase):
    def test_geoip(self):
        with self.app.test_client() as client:
            result = client.get(
                'api/geonames/geoip',
            )
            response = result.get_json()
            self.assertEqual(
                response['data']['city'],
                'West New York'
            )
            self.assertEqual(
                response['data']['iso2'],
                'us'
            )

    def test_within(self):
        with self.app.test_client() as client:
            # send data as GET form to endpoint
            sent = {'iso2': 'us', 'lon': '-74.0096', 'lat': '40.7924'}
            result = client.get(
                'api/geonames/within',
                query_string=sent
            )
            response = result.get_json()
            self.assertTrue(response['success'])
            self.assertTrue(response['data']['within'])
            self.assertEqual(
                response['data']['data']['iso2'],
                'US'
            )

    def test_reverse_geocode(self):
        with self.app.test_client() as client:
            # send data as GET form to endpoint
            sent = {'lon': '-74.01', 'lat': '40.78'}
            result = client.get(
                'api/geonames/reverse-geocode',
                query_string=sent
            )
            response = result.get_json()
            self.assertEqual(
                response['data'][0]['properties']['name'],
                'West New York'
            )
            self.assertEqual(
                response['data'][0]['properties']['admin1'],
                'New Jersey'
            )
            self.assertEqual(
                response['data'][0]['properties']['iso2'],
                'US'
            )

    def test_geocode(self):
        with self.app.test_client() as client:
            # send data as GET form to endpoint
            sent = {'iso2': 'us', 'name': 'Saratoga', 'admin1': 'New York'}
            result = client.get(
                'api/geonames/geocode',
                query_string=sent
            )
            response = result.get_json()
            self.assertEqual(
                response['data'][0]['properties']['iso2'],
                'US'
            )
            self.assertEqual(
                response['data'][0]['properties']['name'],
                'Saratoga Springs'
            )
            self.assertEqual(
                response['data'][0]['properties']['admin1'],
                'New York'
            )

    def test_geocode_with_single_line_input(self):
        with self.app.test_client() as client:
            # send data as GET form to endpoint
            sent = {'iso2': 'us', 'text': 'Saratoga Springs'}
            result = client.get(
                'api/geonames/geocode',
                query_string=sent
            )
            response = result.get_json()
            self.assertEqual(
                response['data'][0]['properties']['iso2'],
                'US'
            )
            self.assertTrue(len(response['data']) > 1)
            sent = {'iso2': 'us', 'text': 'Saratoga Springs, New'}
            result = client.get(
                'api/geonames/geocode',
                query_string=sent
            )
            response = result.get_json()
            self.assertEqual(
                response['data'][0]['properties']['iso2'],
                'US'
            )
            self.assertEqual(len(response['data']), 1)
