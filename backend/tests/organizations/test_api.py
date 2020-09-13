import json

from api.organizations.models import Organization
from tests.auth.test_auth import login_user
from tests.base import BaseTestCase

insert_org = dict(
    name='ABC Company',
    headline='My awesome Company',
    yearFounded=1982,
    size='200-1000',
    # logo = db.Column(db.String)
    url='https://www.google.com/ab-company?test=1',
    description='1' * 1000,
    sector='public',
    contactName='John Smith',
    contactPhone='518-727-8244',
    contactEmail='jsmith@gmail.com',

    # admin
    dataSource='gjm',

    # location
    hiresRemote=True,
    isDistributed=True,
    streetAddress='30 Fairway blvd',
    postalCode='12831',
    city='Gansevoort',
    state='NY',
    countryCode='US',
    lon='-73.762967',  # wilton
    lat='43.147556'
)


class TestOrgApi(BaseTestCase):

    def test_organization_insert_not_logged_in(self):
        with self.app.test_client() as client:
            result = client.post(
                'api/organizations/add',
                data=json.dumps(insert_org),
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

    def test_organization_insert_is_logged_in(self):
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            result = client.post(
                'api/organizations/add',
                data=json.dumps(insert_org),
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
            org_result = Organization.query.filter_by(id=response['id']).first()

            self.assertEqual(org_result.slug, 'abc-company')
            self.assertEqual(org_result.formatted_location, 'Gansevoort, NY')

    def test_organization_update_logged_in(self):
        """Update a organization while logged in"""
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            add_result = client.post(
                'api/organizations/add',
                data=json.dumps(insert_org),
                headers=headers,
                content_type='application/json',
            )
            add_response = add_result.get_json()
            update_result = client.post(
                'api/organizations/update',
                data=json.dumps({'id': add_response['id'], 'name': '123 company'}),
                headers=headers,
                content_type='application/json',
            )
            response = update_result.get_json()
            self.assertEqual(
                update_result.status_code,
                200
            )
            self.assertEqual(
                response['success'],
                True
            )
            org_result = Organization.query.filter_by(id=response['id']).first()
            self.assertEqual(org_result.slug, '123-company')

    def test_organization_update_not_logged_in(self):
        with self.app.test_client() as client:
            result = client.post(
                'api/organizations/update',
                data=json.dumps({'company': '123 company'}),
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
            self.assertEqual(
                response['message'],
                'Provide a valid auth token.'
            )

    def test_organization_get_all(self):
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            client.post(
                'api/organizations/add',
                data=json.dumps(insert_org),
                headers=headers,
                content_type='application/json',
            )
            result = client.get(
                'api/organizations/all',
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
                response['data']['type'],
                'FeatureCollection'
            )
            self.assertEqual(
                response['data']['features'][0]['properties']['slug'],
                '1-abc-company'
            )

    def test_organization_get_detail(self):
        with self.app.test_client() as client:
            response = login_user(self, self.admin_user, self.admin_pass)
            data = json.loads(response.data.decode())
            token = data['auth_token']
            headers = {
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/json'
            }
            client.post(
                'api/organizations/add',
                data=json.dumps(insert_org),
                headers=headers,
                content_type='application/json',
            )
            result = client.get(
                'api/organizations/detail',
                data=json.dumps({'id': 1}),
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
                response['data']['properties']['slug'],
                '1-abc-company'
            )