from tests.base import BaseTestCase
from api import db
from api.jobs.models import Job
from api.tags.models import Tag


class TestJobsApiViewAll(BaseTestCase):
    def test_job_view_all(self):
        """ View all jobs """
        t1 = Tag.get_or_create(name='qgis')
        t2 = Tag.get_or_create(name='geoserver')
        t3 = Tag.get_or_create(name='arcmap')
        db.session.add(t1)
        db.session.add(t2)
        db.session.add(t3)

        j1 = Job(
            title='Awesome Job',
            company="ABC Company",
            tags=[t1, t2],
            contact_email="test@abccompany.com",
            lat=50.039,
            lon=-97.313,
            country_code="ca",
            data_source='indeed',
            formatted_location='Winnipeg, Manitoba',
            is_remote=0
        )


        j2 = Job(
            title='Cool Gig',
            company="123 Organization",
            tags=[t1, t3, t2],
            contact_email="test@abccompany.com",
            lat=48.000,
            lon=-97.2259,
            country_code="US",
            data_source='gjm',
            formatted_location='Grand Forks, North Dakota',
            is_remote=0
        )

        # remote canadian job
        j3 = Job(
            title='Cool Gig 2',
            company="123 Organization",
            tags=[t1, t3, t2],
            contact_email="test@abccompany.com",
            lat=45.4158,
            lon=-75.8575,
            country_code="ca",
            formatted_location='Ottawa, Ontario',
            data_source='indeed',
            is_remote=1
        )

        # remote us job
        j4 = Job(
            title='Remote Job 2',
            company="Cool Organization",
            tags=[t1, t3, t2],
            contact_email="test@abccompany.com",
            lat=42.1114,
            lon=-75.9505,
            country_code="US",
            data_source='indeed',
            formatted_location='Binghamton, New York',
            is_remote=1
        )

        db.session.add(j1)
        db.session.add(j2)
        db.session.add(j3)
        db.session.add(j4)
        db.session.commit()

        with self.app.test_client() as client:
            sent = dict(
                box='-103.57,46.10,-91.06,53.68',  # Center of Canadian border with Grand Forks and Winnipeg in bounds.
                maponly='true',
                )
            result = client.get(
                'api/jobs/all',
                query_string=sent,
            )
            response = result.get_json()
            self.assertEqual(
                result.status_code,
                200
            )
            self.assertTrue(response['success'])
            self.assertEqual(len(response['data']), 2)
            self.assertEqual(response['data'][0]['properties']['formattedLocation'], 'Winnipeg, Manitoba')
            self.assertEqual(response['data'][1]['properties']['formattedLocation'], 'Grand Forks, North Dakota')

            sent = dict(
                box='-103.57,46.10,-91.06,53.68',
            )
            result = client.get(
                'api/jobs/all',
                query_string=sent,
            )

            response = result.get_json()

            self.assertEqual(
                result.status_code,
                200
            )
            self.assertTrue(response['success'])
            self.assertEqual(len(response['data']), 4)

