from tests.base import BaseTestCase


class TestTagApi(BaseTestCase):

    def test_get_all_valid_categories(self):
        """ Get all categories from api """
        with self.app.test_client() as client:
            result = client.get(
                'api/categories/all',
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

    def test_get_valid_categories_with_query(self):
        """ Get categories with query """
        with self.app.test_client() as client:
            result = client.get(
                'api/categories/all',
                query_string={'search': 'data-science'},
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