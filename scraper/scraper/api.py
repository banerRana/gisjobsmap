import json
import logging
import os
import time

import requests

logging.basicConfig(level=logging.ERROR, filename='scraper.log', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataAPI():

    def __init__(self):
        self.token = None
        self.base_url = 'http://backend:5000/api'
        self.categories = []
        self.tags = []

        self.current_active = []
        self.valid_active = []
        self.valid_inactive = []
        self.invalid = []
        self.new_invalid = []
        # Login and get reference data
        self.login()
        self.init_data()

    def init_data(self):
        try:
            time.sleep(1)  # prevent max requests exceeded error
            self.get_categories()
            time.sleep(1)
            self.get_tags()
            time.sleep(1)
            self.get_invalid_jobkeys()
            time.sleep(1)
            return True
        except Exception as e:
            logging.error('Initializing data failed.', e)

    def test_geo(self):
        try:
            """returns a geocoded dictionary"""
            payload = {'name': 'Saratoga', 'iso2': 'us'}
            r = requests.get("{}/geonames/geocode".format(self.base_url), params=payload)
            data = r.json()
            if not len(data['data']):
                raise Exception("Geocode api error: no data returned")
            return True
        except Exception as e:
            print('testing the geonames database failed.')

    def login(self):
        r = requests.post(
            '{}/auth/login'.format(self.base_url),
            data=json.dumps(dict(
                email=os.environ.get('SCRAPE_USER'),
                password=os.environ.get('ACCOUNT_PASSWORD')
            )),
            headers={'Content-type': 'application/json'}
        )
        data = r.json()
        token = data.get('auth_token')
        msg = data.get('message')
        if token:
            self.token = token
        else:
            raise Exception('Login Error: {}. {}'.format(r.status_code, msg))

    def logout(self):
        r = requests.post(
            '{}/auth/logout'.format(self.base_url),
            headers={
                'Authorization': 'Bearer ' + self.token,
                'Content-type': 'application/json'
            }
        )
        if r.status_code == 200:
            self.token = None
        else:
            raise Exception('Logout error: {}'.format(r.status_code))

    def set_active_inactive(self, keys, task):
        """sends a list of job keys that are inactive"""
        payload = {'keys': list(set(keys)), 'task': task}
        r = requests.post("{}/jobs/inactive".format(self.base_url),
                          data=json.dumps(payload, indent=4, sort_keys=True, default=str),
                          headers={'Authorization': 'Bearer ' + self.token,
                                   'Content-type': 'application/json'})
        if r.status_code != 200:
            raise Exception('Set Inactive Jobs Error: {}'.format(r.status_code))

    def add_valid_job(self, payload):
        """sends a new job"""
        r = requests.post('{}/jobs/add'.format(self.base_url),
                          data=json.dumps(payload, indent=4, sort_keys=True, default=str),
                          headers={'Authorization': 'Bearer ' + self.token,
                                   'Content-type': 'application/json'})

        if r.status_code != 200:
            raise Exception('Add Job Error: {}. {}'.format(r.status_code, r.text))

    def get_invalid_jobkeys(self):
        """Returns a list of invalid job keys"""
        r = requests.get("{}/scraper/invalid".format(self.base_url),
                         headers={'Authorization': 'Bearer ' + self.token,
                                  'Content-type': 'application/json'})
        response = r.json()
        if r.status_code != 200:
            logging.error('invalid job keys error', response)
            raise Exception('Get Invalid Job Keys Error: {}'.format(r.status_code))
        self.invalid = response['keys']

    def get_valid_jobkeys(self, country_code):
        """Returns a list of valid job keys"""
        r = requests.get("{}/jobs/valid".format(self.base_url),
                         data=json.dumps({'iso2': country_code}, indent=4, sort_keys=True, default=str),
                         headers={'Authorization': 'Bearer ' + self.token,
                                  'Content-type': 'application/json'})
        response = r.json()
        if r.status_code != 200:
            raise Exception('Get Valid Job Keys Error: {}'.format(r.status_code))
        self.valid_active.extend(response['active'])
        self.valid_inactive.extend(response['inactive'])

    def add_invalid_jobkeys(self, keys):
        """Sends a list of invalid job keys"""
        payload = {'keys': list(set(keys))}
        r = requests.post("{}/scraper/invalid".format(self.base_url),
                          data=json.dumps(payload, indent=4, sort_keys=True, default=str),
                          headers={'Authorization': 'Bearer ' + self.token,
                                   'Content-type': 'application/json'})
        response = r.json()
        if r.status_code != 200:
            logger.error('Add Invalid Job Keys Error: {}'.format(response['message']))
            raise Exception('Add Invalid Job Keys Error: {}'.format(r.status_code))

    def set_status(self, payload):
        """sends a completed status result"""
        r = requests.post('{}/scraper/status'.format(self.base_url),
                          data=json.dumps(payload, indent=4, sort_keys=True, default=str),
                          headers={
                              'Authorization': 'Bearer ' + self.token,
                              'Content-type': 'application/json'
                          })
        if r.status_code != 200:
            raise Exception('Set Status Error: {}'.format(r.status_code))

    def get_categories(self):
        """Returns a list of categories """
        r = requests.get("{}/categories/all".format(self.base_url),
                         headers={
                             'Authorization': 'Bearer ' + self.token,
                             'Content-type': 'application/json'
                         })
        if r.status_code == 200:
            data = r.json()
            self.categories = data['data']
        else:
            raise Exception('Get Categories Error: {}'.format(r.status_code))

    def get_tags(self):
        """returns a list of tags"""
        r = requests.get("{}/tags/all".format(self.base_url),
                         headers={'Content-type': 'application/json'
                                  })
        if r.status_code == 200:
            data = r.json()
            self.tags = data['data']
        else:
            raise Exception('Get Tags Error: {}'.format(r.status_code))
