from tests.base import BaseTestCase
from api.tags.models import Tag


class TestTagModel(BaseTestCase):

    def test_tags_query_has_results(self):
        """ testing for valid results from Tag Model"""
        query = Tag.query.all()
        self.assertTrue(len(query) > 0)

