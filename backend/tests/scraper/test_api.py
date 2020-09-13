import json
from api import db
from api.scraper.models import Invalid, Status
from tests.base import BaseTestCase
from tests.auth.test_auth import login_user
from datetime import datetime

test_keys = ['123456780', '123456781', '123456782', '123456783', '123456784', '123456785', '123456786']

test_status = {
    'time_start': datetime.utcnow(),
    # 'time_end': None,
    'errors': 2,
    'is_success': True,
    'messages': 'test message',
    'new': 32,
    'expired': 1,
    'total_valid': 2,
    'processed': 4
}


class TestScraperAPI(BaseTestCase):
    def test_add_invalid_jobkeys_not_logged_in(self):
        """Insert invalid keys NOT logged in"""
        invalid_keys = dict(keys=['123456780', '123456781', '123456782', '123456783', '123456784', '123456785', '123456786'])
        with self.app.test_client() as client:
            result = client.post(
                'api/scraper/invalid',
                data=json.dumps(invalid_keys),
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

    def test_add_invalid_jobkeys_logged_in(self):
        """Insert invalid keys logged in"""
        invalid_keys = dict(keys=test_keys)
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            result = client.post(
                'api/scraper/invalid',
                data=json.dumps(invalid_keys),
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
            keys = db.session.query(Invalid.key).all()
            self.assertEqual(
                len(keys),
                len(test_keys)
            )

    def test_get_invalid_jobkeys(self):
        with self.app.test_client() as client:
            Invalid.bulk_add(keys=test_keys)
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            result = client.get(
                'api/scraper/invalid',
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
            self.assertEqual(
                len(response['keys']),
                len(test_keys)
            )
            assert type(response['keys'][0]) == str

    def test_add_status(self):
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            result = client.post(
                'api/scraper/status',
                data=json.dumps(test_status, indent=4, sort_keys=True, default=str),
                headers=headers,
                content_type='application/json',
            )

            response = result.get_json()

            result = db.session.query(Status).first()
            self.assertEqual(
                result.messages,
                test_status['messages']
            )
            self.assertEqual(
                response['success'],
                True
            )


    def test_get_status(self):
        """ will be accessible through admin interface """
        pass
