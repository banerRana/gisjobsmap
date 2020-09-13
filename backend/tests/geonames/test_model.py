import unittest
import json
from tests.base import BaseTestCase
from api.geonames.models import Geoname, WorldBorders


class TestGeonamesModel(BaseTestCase):
    # def test_geocode(self):
    #     result = Geoname.geocode(iso2='de', name='berlin')
    #     assert len(result) > 2
    #     for r in result:
    #         assert len(r["properties"]["admin1"])
    #
    # def test_reverse_geocode(self):
    #     result = Geoname.reverse_geocode(lat=43.610, lon=-72.972)
    #     self.assertEqual(result[0]['properties']['name'], 'Rutland')
    #     self.assertEqual(result[0]['properties']['admin1'], 'Vermont')
    #     self.assertEqual(result[0]['properties']['iso2'], 'US')
    #     self.assertEqual(len(result[0]['geometry']['coordinates']), 2)
    #
    #     result = Geoname.reverse_geocode(lat=53.20, lon=-2.92)
    #     self.assertEqual(result[0]['properties']['name'], 'Blacon')
    #     self.assertEqual(result[0]['properties']['admin1'], 'England')
    #     self.assertEqual(result[0]['properties']['iso2'], 'GB')
    #     self.assertEqual(len(result[0]['geometry']['coordinates']), 2)
    #
    #     # 41.07365737372555, lng: -73.76976013183595
    #     result = Geoname.reverse_geocode(lat=41.07365737372555, lon=-73.76976013183595, min_population=100000)
    #     # print(result)
    #     # self.assertEqual(result[0]['properties']['name'], 'Blacon')
    #     # self.assertEqual(result[0]['properties']['admin1'], 'England')
    #     # self.assertEqual(result[0]['properties']['iso2'], 'GB')
    #     # self.assertEqual(len(result[0]['geometry']['coordinates']), 2)
    #
    # def test_within_country_bounds(self):
    #     """tests if point falls within a countries boundary"""
    #     result = WorldBorders.is_within(iso2='us', lat=43.60, lon=-72.98)
    #     self.assertTrue(result['within'])
    #     self.assertEqual(result['data']['iso2'], 'US')
    #
    #     result = WorldBorders.is_within(iso2='gb', lat=53.17392, lon=-2.9365)
    #     self.assertTrue(result['within'])
    #     self.assertEqual(result['data']['iso2'], 'GB')
    #
    # def test_within_country_coast(self):
    #     """tests if point falls within a countries at the coast"""
    #     # nags head, NC - 35.964846, -75.622398
    #     result = WorldBorders.is_within(iso2='us', lat=35.964846, lon=-75.622398)
    #     self.assertTrue(result['within'])
    #     self.assertEqual(result['data']['iso2'], 'US')
    #
    #     # Galway, IE - 53.252897, -9.061641
    #     result = WorldBorders.is_within(iso2='ie', lat=53.252897, lon=-9.061641)
    #     self.assertTrue(result['within'])
    #     self.assertEqual(result['data']['iso2'], 'IE')
    #
    # def test_within_country_fail(self):
    #     """tests within country failure"""
    #     # Atlantic Ocean off Irish Coast
    #     result = WorldBorders.is_within(iso2='ie', lat=52.819235, lon=-10.289262)
    #     self.assertFalse(result['within'])

    # def test_get_country_from_bounding_box_centroid(self):
    #     # NYS: -80.75%2C40.43%2C-70.81%2C44.77
    #     # Canada/NYS: -75.57%2C43.93%2C-70.60%2C46.01
    #     # USA Eastern seaboard  # -83.13%2C36.50%2C-76.09%2C41.10
    #     # UK/IReland -13.49%2C50.86%2C0.59%2C57.73
    #     # -93.95,51.64,167.79,82.34
    #     # Nevada: -163.17%2C-9.63%2C-63.15%2C64.32  center: lat: 35.0946173393393 lng: -113.15667704036598
    #     result = WorldBorders.countries_from_bounding_box(box='-83.13,36.50,-76.09,41.10')
    #     self.assertEqual(result, 'us')
    #
    #     result = WorldBorders.countries_from_bounding_box(box='-163.17,-9.63,-63.15,64.32')
    #     self.assertEqual(result, 'us')
    #
    #     result = WorldBorders.countries_from_bounding_box(box='-13.49,50.86,0.59,57.73')
    #     self.assertEqual(result, 'gb')
    #
    #     result = WorldBorders.countries_from_bounding_box(box='-104.94,25.49,-54.93,59.04')
    #     self.assertEqual(result, 'ca')

        # Not canada:
        # -179.83,-4.50,81.91,66.47
    def test_get_countries_from_bouding_box(self):
        result = WorldBorders.countries_from_bounding_box(box='-9.68,51.24,0.26,54.78')
        self.assertEqual(result, ['ie', 'im', 'gb'])

    # def test_country_geom_dump(self):
    #     result = WorldBorders.get_country_geometry('us')
    #     geojson_data = json.loads(result)
    #     self.assertEqual('MultiPolygon', geojson_data['type'])
    #     self.assertTrue(len(geojson_data['coordinates']) > 1)
