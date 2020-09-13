import json
from api import db
from tests.base import BaseTestCase

from api.jobs.models import Job
from api.categories.models import Category
from api.tags.models import Tag
from tests.auth.test_auth import login_user


class TestJobsApiUpdate(BaseTestCase):

    def test_job_update_logged_in(self):
        """ Update a job while logged in """
        with self.app.test_client() as client:
            new_job = Job(user_id=1, title='123 Job',
                          tags=[Tag.get_or_create(name="qgis"),
                                Tag.get_or_create(name="geoserver")],
                          categories=[Category.get_or_create(name="cartographer"),
                                      Category.get_or_create(name="software-engineer")]
                          )
            db.session.add(new_job)
            db.session.commit()
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            result = client.post(
                'api/jobs/update',
                data=json.dumps({'id': new_job.id,
                                 'title': 'Abc Gig',
                                 'tags': ['qgis', 'esri', 'geoserver'],
                                 'categories': ['data-science', 'software-engineer']}),
                headers=headers,
                content_type='application/json',
            )
            response = result.get_json()
            self.assertEqual(
                result.status_code,
                200
            )
            self.assertEqual(
                response['success'],
                True
            )
            query_result = Job.query_from_slug(response['id'])
            self.assertEqual(query_result.slug, 'abc-gig')
            self.assertEqual(len(query_result.tags), 3)
            self.assertTrue('qgis' in [t.name for t in query_result.tags])
            self.assertTrue('esri' in [t.name for t in query_result.tags])
            self.assertTrue('geoserver' in [t.name for t in query_result.tags])
            self.assertTrue('geoserver' in [t.name for t in query_result.tags])
            self.assertEqual(len(query_result.categories), 2)
            self.assertTrue('data-science' in [t.name for t in query_result.categories])
            self.assertTrue('software-engineer' in [t.name for t in query_result.categories])

    def test_job_update_not_logged_in(self):
        """ Update a Job while NOT logged in """
        with self.app.test_client() as client:
            result = client.post(
                'api/jobs/update',
                data=json.dumps({'company': '123 company'}),
                content_type='application/json',
            )
            response = result.get_json()
            self.assertFalse(
                response['success']
            )
            self.assertEqual(
                result.status_code,
                403
            )

    def test_update_jobs_inactive(self):
        """ set jobs inactive by indeed-key. Requires admin user rights. """
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            db.session.add(Job(indeed_key="123456", company="123 company", data_source='indeed', is_active=True))
            db.session.add(Job(indeed_key="123455", company="ABC organization", data_source='indeed', is_active=True))
            db.session.add(Job(indeed_key="123454", company="XYZ corporation", data_source='indeed'))
            db.session.add(Job(indeed_key="123453", company="XYZ corporation", data_source='gjm', is_active=True))
            db.session.commit()
            result = client.post(
                'api/jobs/inactive',
                data=json.dumps({'keys': ['123456', '123455', '123453'], 'task':'inactive'}),
                headers=headers,
                content_type='application/json',
            )
            response = result.get_json()
            self.assertTrue(
                response['success']
            )
            self.assertEqual(
                result.status_code,
                200
            )
            query_result = db.session.query(Job).order_by(Job.indeed_key.desc()).all()
            self.assertFalse(
                query_result[0].is_active
            )
            self.assertFalse(
                query_result[1].is_active
            )
            self.assertTrue(
                query_result[2].is_active
            )
            self.assertTrue(
                query_result[3].is_active
            )

            result = client.post(
                'api/jobs/inactive',
                data=json.dumps({'keys': ['123456', '123455', '123453'], 'task':'active'}),
                headers=headers,
                content_type='application/json',
            )
            response = result.get_json()
            self.assertTrue(
                response['success']
            )
            self.assertEqual(
                result.status_code,
                200
            )
            query_result = db.session.query(Job).order_by(Job.indeed_key.desc()).all()
            self.assertTrue(
                query_result[0].is_active
            )
            self.assertTrue(
                query_result[1].is_active
            )
            self.assertTrue(
                query_result[2].is_active
            )
            self.assertTrue(
                query_result[3].is_active
            )

    def test_update_jobs_inactive_by_indeed_keys(self):
        pass

