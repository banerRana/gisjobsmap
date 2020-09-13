import unittest
from api import db
from tests.base import BaseTestCase
from api.organizations.models import Organization
from api.auth.models import User
from api.tags.models import Tag


class TestOrgModel(BaseTestCase):

    def test_new_org_admin(self):
        new_org = Organization(
            user_id=User.query.filter_by(email=self.admin_user).first().id,
            name='ABC Company',
            headline='My awesome Company',
            year_founded=1982,
            size=200 - 1000,
            # logo = db.Column(db.String)
            url='https://www.google.com/ab-company?test=1',
            description='This is an aweseom place \n' * 50,
            sector='public',
            contact_name='John Smith',
            contact_phone='518-727-8244',
            contact_email='jsmith@gmail.com',

            # admin
            is_sponsor=True,
            data_source='gjm',

            # location
            hires_remote=True,
            is_distributed=True,
            street_address='30 Fairway blvd',
            postal_code='12831',
            city='Gansevoort',
            state='NY',
            country_code='US',
            lon='-73.762967',  # wilton
            lat='43.147556')

        db.session.add(new_org)
        db.session.commit()
        assert new_org.invalid_geom == False
        assert new_org.name == 'ABC Company'
        assert new_org.slug == 'abc-company'
        assert new_org.formatted_location == 'Gansevoort, NY'

    def test_invalid_geom(self):
        new_org = Organization(user_id=User.query.filter_by(email=self.admin_user).first().id,
                               country_code='us',
                               lon='0',
                               lat='0')
        db.session.add(new_org)
        db.session.commit()
        assert new_org.invalid_geom == True

    def test_tags_relation(self):
        tag1 = Tag(name='Python')
        tag2 = Tag(name='R')
        tag3 = Tag(name='Javascript')
        new_job = Organization(user_id=User.query.filter_by(email=self.admin_user).first().id,
                               tags=[tag1, tag2, tag3])
        db.session.add(new_job)
        db.session.commit()
        assert len(new_job.tags) == 3


if __name__ == '__main__':
    unittest.main()
