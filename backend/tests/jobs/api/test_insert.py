import json
from tests.base import BaseTestCase
from api.jobs.models import Job
from tests.auth.test_auth import login_user
from .fake_data import insert_job


class TestJobsApiInsert(BaseTestCase):
    def test_job_api_insert_not_logged_in(self):
        """ Insert a job NOT logged in """
        with self.app.test_client() as client:
            result = client.post(
                'api/jobs/add',
                data=json.dumps(insert_job),
                content_type='application/json',
            )
            response = result.get_json()
            self.assertEqual(
                result.status_code,
                403
            )
            self.assertEqual(
                response['success'],
                False
            )

    def test_job_api_insert_is_logged_in(self):
        """ Insert a job while logged in """
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            result = client.post(
                'api/jobs/add',
                data=json.dumps(insert_job),
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
            job_result = Job.query_from_slug(response['id'])
            self.assertEqual(
                job_result.data_source,
                'gjm'
            )
            self.assertEqual(
                job_result.compensation,
                '100,000 USD'
            )

    def test_job_api_insert_with_categories_and_tags(self):
        """ test inserting categories with a job """
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            insert_job['tags'] = ['qgis', 'geoserver']
            insert_job['categories'] = ['software-engineer', 'cartography']
            result = client.post(
                'api/jobs/add',
                data=json.dumps(insert_job),
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
            result = Job.query_from_slug(response['id'])
            self.assertEqual(len(result.tags), len(insert_job['tags']))
            self.assertEqual(len(result.categories), len(insert_job['categories']))
