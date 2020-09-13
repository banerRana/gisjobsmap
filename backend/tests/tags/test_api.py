from tests.base import BaseTestCase
# from api.organizations.models import Organization
# from api.jobs.models import Job
# from api.tags.models import Tag


class TestTagApi(BaseTestCase):

    def test_get_all_valid_tags(self):
        """ Get all tags from api """
        with self.app.test_client() as client:
            result = client.get(
                'api/tags/all',
                content_type='application/json',
            )
            response = result.get_json()
            self.assertEqual(
                result.status_code,
                200
            )
            self.assertTrue(
                response['success']
            )
            self.assertTrue(
                len(response['data'])
            )

    def test_get_valid_tags_with_query(self):
        """ Get tags with query """
        with self.app.test_client() as client:
            result = client.get(
                'api/tags/all',
                query_string={'search': 'qgis'},
                content_type='application/json',
            )
            response = result.get_json()
            self.assertEqual(
                result.status_code,
                200
            )
            self.assertTrue(
                response['success']
            )
            self.assertEqual(
                len(response['data']), 1
            )