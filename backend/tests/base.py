import os
from flask_testing import TestCase
from api import create_app, db
from api.auth.models import User
from api.tags.models import Tag
from api.categories.models import Category

app = create_app()


class BaseTestCase(TestCase):

    def assertDictSubsetEqual(self, subset, superset):
        for k, v in subset.items():
            self.assertEqual(v, superset[k], k)

    @classmethod
    def create_app(cls):
        cls.admin_user = os.getenv('ADMIN_USER')
        cls.admin_pass = os.getenv('ACCOUNT_PASSWORD')
        cls.reg_user = 'anonymous@anonymous.com'
        cls.reg_pass = os.getenv('ACCOUNT_PASSWORD')
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all(bind=None)
        admin_user = User(email=self.admin_user,
                          password=self.admin_pass,
                          confirmed=True,
                          admin=True)
        db.session.add(admin_user)
        user = User(email=self.reg_user,
                    password=self.reg_pass,
                    confirmed=True)
        db.session.add(user)

        categories = ['data-science', 'software-engineer', 'research', 'consultant', 'geology']
        tags = ['qgis', 'esri', 'geoserver', 'gdal', 'carto', 'arcgis-pro', 'mapbox']

        for t in tags:
            new_tag = Tag(
                valid=True,
                name=t,
                gis=1
            )
            db.session.add(new_tag)
            # db.session.commit()

        for c in categories:
            new_tag = Category(
                valid=True,
                name=c,
            )
            db.session.add(new_tag)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all(bind=None)
