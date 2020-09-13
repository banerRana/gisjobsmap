from unittest import TestCase

from scraper.utils import find_categories, find_tags, is_valid_title, get_soup


class TestUtils(TestCase):

    def test_is_valid_title(self):
        self.assertTrue(is_valid_title('gis specialist'))
        self.assertTrue(is_valid_title('gis developer II'))
        self.assertTrue(is_valid_title('Spatial database administratio'))
        self.assertFalse(is_valid_title('database administratio'))
        self.assertFalse(is_valid_title(None))

    def test_get_tags(self):
        tags = [
            {'name': 'arcgis-pro', 'gis': 1},
            {'name': 'geokettle', 'gis': 1},
            {'name': 'c++', 'gis': 0},
            {'name': 'r', 'gis': 0},
            {'name': 'rust', 'gis': 0},
            {'name': 'survey123', 'gis': 0},
            {'name': 'security-clearance', 'gis': 0},
            {'name': '.net', 'gis': 0},
            {'name': 'qgis', 'gis': 1},
        ]
        soup = "<div>This is a test of geokettle, qgis and c++ in gis</div>"
        result = find_tags(soup, tags)
        self.assertTrue(result['gis_specific'])
        self.assertListEqual(sorted(['geokettle', 'c++', 'qgis']), sorted(result['tags']))

        result = find_tags('random record of relational rrrr\'s', tags)
        self.assertListEqual([], result['tags'])

        result = find_tags('languagaes including r, c++, rust, and more', tags)
        self.assertListEqual(sorted(['r', 'c++', 'rust']), sorted(result['tags']))

        result = find_tags('security clearance and arcgis pro and maps', tags)
        self.assertListEqual(sorted(['arcgis-pro', 'security-clearance']), sorted(result['tags']))

        result = find_tags(None, tags)
        self.assertListEqual(result['tags'], [])

        # test return limit
        result = find_tags('qgis w/ arcgis pro, cartography, c++, r, rust, survey123, geokettle and .net', tags)
        self.assertEqual(len(result['tags']), 7)

        # test gis specific
        result = find_tags('arcgis pro and .net', tags)
        self.assertFalse(result['gis_specific'])

        result = find_tags('rust and .net', tags)
        self.assertFalse(result['gis_specific'])

    def test_get_categories(self):
        categories = [{'name': 'education', 'searches': 'trainer;instructor;professor;teacher;lecturer'},
                      {'name': 'data-science', 'searches': 'data scientist;data science'},
                      {'name': 'entry-level', 'searches': 'fellowship;fellow;intern;internship;entry level'},
                      {'name': 'software-engineer', 'searches': 'software engineer;software engineering'},
                      {'name': 'postdoctoral', 'searches': 'postdoctoral;phd'},
                      {'name': 'other', 'searches': ''}]

        # categories = [Category(c) for c in category_data]

        result = find_categories('lecturer adjunct', categories)
        self.assertListEqual(result, ['education'])

        result = find_categories('entry level data scientist', categories)
        self.assertListEqual(sorted(result), sorted(['entry-level', 'data-science']))

        result = find_categories('', categories)
        self.assertListEqual(result, ['other'])

        result = find_categories(None, categories)
        self.assertListEqual(result, ['other'])

        # test return limit
        result = find_categories('software engineering internship with a phd in cartography', categories)
        self.assertEqual(len(result), 3)

    def test_soup_extraction(self):
        text = get_soup(file='')
        self.assertEqual(text, None)

        text = get_soup(file=None)
        self.assertEqual(text, None)

        with open('tests/gis-developer.html', 'rb') as html:
            webpage = html.read().decode("UTF-8")
        text = get_soup(file=webpage)
        self.assertTrue(
            text.startswith("Description:\n\nManagement consulting firm specializing in Big Data, is seeking experienced"))
        self.assertTrue(
            text.endswith("and technical support specialists"))
        self.assertTrue(len(text) > 150)
        # self.assertEqual(text, match_string)

        with open('tests/gis-database-administrator.html', 'rb') as html:
            webpage = html.read()
        text = get_soup(file=webpage)
        self.assertTrue(
            text.startswith("Introduction\n\nPrince William County GIS, a well-established GIS program and winners of"))
        self.assertTrue(
            text.endswith("Check, and/or Fingerprinting may be required as posted in the job advertisement."))
        self.assertTrue(len(text) > 150)
        # self.assertEqual(text, match_string)
