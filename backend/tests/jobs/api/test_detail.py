import datetime
from api import db
from tests.base import BaseTestCase
from api.auth.models import User
from api.jobs.models import Job
from api.categories.models import Category
from api.tags.models import Tag


class TestJobsApiDetail(BaseTestCase):

    def test_job_detail_by_slug(self):
        """ Get job detail by slug """
        new_job = Job(indeed_key='6f93d0276d96a980',
                      user_id=User.query.filter_by(email=self.admin_user).first().id,
                      title='Awesome Job Title',
                      company='Nearmap',
                      # snippet=snippet,
                      city='Crystal City',
                      state='VA',
                      country_code='us',
                      formatted_location='Crystal City, VA',
                      publish_date=datetime.datetime(2019, 9, 28, 18, 22, 43),
                      url='http://www.indeed.com/viewjob?jk=6f93d0276d96a980&qd=I2j7AToAjJ5zNIEXXC-b31pdQoS7Su7RBUeDL1UDx8SL695KK9_wWL18-RAD0qU5EiK4cRUNKnQsaMbvwjWMaeoCFLMibOCEabUahnuewCk&indpubnum=4327070819127165&atk=1dn68qp3oo96p800',
                      data_source='indeed',
                      tags=[Tag.get_or_create(name='qgis'), Tag.get_or_create(name='geoserver')],
                      categories=[Category.get_or_create(name='data-science'), Category.get_or_create(name='cartography')],
                      description='<div class="jobsearch-JobComponent-description icl-u-xs-mt--md"><div class="jobsearch-jobDescriptionText" id="jobDescriptionText"><div><p>Nearmap is  ... (3703 characters truncated) ... armap, we invite you to come and make a difference!</p><br/>\n<p></p>\n<p><i>\nEqual Opportunity Employer/Veterans/Disabled</i></p></div></div></div>',
                      is_remote=0,
                      lon='-73.762967',  # wilton
                      lat='43.147556'
                      )
        db.session.add(new_job)
        db.session.commit()
        with self.app.test_client() as client:
            result = client.get(
                'api/jobs/detail',
                query_string={'slug': '1-awesome-job-title'},
                content_type='application/json',
            )
            response = result.get_json()
            self.assertEqual(
                result.status_code,
                200
            )
            self.assertTrue(response['success'])
            self.assertEqual(response['data']['properties']['slug'], '1-awesome-job-title')
            self.assertEqual(len(response['data']['properties']['tags']), 2)
            self.assertEqual(len(response['data']['properties']['categories']), 2)

    def test_job_detail_by_id(self):
        """ Get job detail by ID """
        new_job = Job(indeed_key='6f93d0276d96a980',
                      user_id=User.query.filter_by(email=self.admin_user).first().id,
                      title='Awesome Job Title',
                      company='Nearmap',
                      city='Crystal City',
                      state='VA',
                      country_code='us',
                      formatted_location='Crystal City, VA',
                      publish_date=datetime.datetime(2019, 9, 28, 18, 22, 43),
                      url='http://www.indeed.com/viewjob?jk=6f93d0276d96a980&qd=I2j7AToAjJ5zNIEXXC-b31pdQoS7Su7RBUeDL1UDx8SL695KK9_wWL18-RAD0qU5EiK4cRUNKnQsaMbvwjWMaeoCFLMibOCEabUahnuewCk&indpubnum=4327070819127165&atk=1dn68qp3oo96p800',
                      data_source='indeed',
                      tags=[Tag.get_or_create(name='qgis'), Tag.get_or_create(name='geoserver')],
                      categories=[Category.get_or_create(name='data-science'), Category.get_or_create(name='cartography')],
                      description='<div class="jobsearch-JobComponent-description icl-u-xs-mt--md"><div class="jobsearch-jobDescriptionText" id="jobDescriptionText"><div><p>Nearmap is  ... (3703 characters truncated) ... armap, we invite you to come and make a difference!</p><br/>\n<p></p>\n<p><i>\nEqual Opportunity Employer/Veterans/Disabled</i></p></div></div></div>',
                      is_remote=0,
                      lon='-73.762967',  # wilton
                      lat='43.147556'
                      )
        db.session.add(new_job)
        db.session.commit()
        with self.app.test_client() as client:
            result = client.get(
                'api/jobs/detail',
                query_string={'id': '1'},
                content_type='application/json',
            )
            response = result.get_json()
            self.assertEqual(
                result.status_code,
                200
            )
            self.assertTrue(response['success'])
            self.assertEqual(response['data']['properties']['slug'], '1-awesome-job-title')
            self.assertEqual(len(response['data']['properties']['tags']), 2)
            self.assertEqual(len(response['data']['properties']['categories']), 2)
