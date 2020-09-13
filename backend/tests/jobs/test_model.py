import datetime
from api import db
from tests.base import BaseTestCase

from api.auth.models import User
from api.jobs.models import Job, job_tags, job_categories
from api.categories.models import Category
from api.tags.models import Tag


class TestJobModel(BaseTestCase):

    def test_new_job(self):
        pub_date = datetime.datetime(2019, 9, 28, 18, 22)
        new_job = Job(indeed_key='6f93d0276d96a980',
                      user_id=User.query.filter_by(email=self.admin_user).first().id,
                      title='Awesome Job Title',
                      company='Nearmap',
                      # snippet=snippet,
                      city='Crystal City',
                      state='VA',
                      country_code='us',
                      formatted_location='Crystal City, VA',
                      publish_date=pub_date,
                      url='http://www.indeed.com/viewjob?jk=6f93d0276d96a980&qd=I2j7AToAjJ5zNIEXXC-b31pdQoS7Su7RBUeDL1UDx8SL695KK9_wWL18-RAD0qU5EiK4cRUNKnQsaMbvwjWMaeoCFLMibOCEabUahnuewCk&indpubnum=4327070819127165&atk=1dn68qp3oo96p800',
                      data_source='indeed',
                      description='<div class="jobsearch-JobComponent-description icl-u-xs-mt--md"><div class="jobsearch-jobDescriptionText" id="jobDescriptionText"><div><p>Nearmap is  ... (3703 characters truncated) ... armap, we invite you to come and make a difference!</p><br/>\n<p></p>\n<p><i>\nEqual Opportunity Employer/Veterans/Disabled</i></p></div></div></div>',
                      is_remote=0,
                      lon='-73.762967',  # wilton
                      lat='43.147556'
                      )

        db.session.add(new_job)
        db.session.commit()
        assert new_job.indeed_key == '6f93d0276d96a980'
        assert new_job.title == 'Awesome Job Title'
        assert new_job.slug == 'awesome-job-title'
        assert new_job.invalid_geom == False
        assert new_job.formatted_location == 'Crystal City, VA'
        assert new_job.publish_date.date() == pub_date.date()

    def test_multiple_jobs_with_same_tags(self):
        """ Tests for adding 2 jobs with the same tags. """
        tag1 = Tag.get_or_create(name="Python")
        tag2 = Tag.get_or_create(name='R')
        tag3 = Tag.get_or_create(name='qgis')
        new_job = Job(indeed_key='6f93d0276d96a981',
                      user_id=User.query.filter_by(email=self.admin_user).first().id,
                      title='Awesome Job Title',
                      tags=[tag1, tag2, tag3]
                      )
        db.session.add(new_job)
        db.session.commit()
        assert len(new_job.tags) == 3

        new_job2 = Job(indeed_key='6f93d0276d96a982',
                       user_id=User.query.filter_by(email=self.admin_user).first().id,
                       title='Awesome Job Title 2',
                       tags=[tag1, tag2, tag3]
                       )
        db.session.add(new_job)
        db.session.commit()
        assert len(new_job2.tags) == 3

    def test_invalid_geom(self):
        new_job = Job(user_id=User.query.filter_by(email=self.admin_user).first().id,
                      country_code='us',
                      lon='0',
                      lat='0')
        db.session.add(new_job)
        db.session.commit()
        assert new_job.invalid_geom == True

    def test_add_tags(self):
        tag1 = Tag.get_or_create(name='Python')
        tag2 = Tag.get_or_create(name='R')
        tag3 = Tag.get_or_create(name='Javascript')
        new_job = Job(user_id=User.query.filter_by(email=self.admin_user).first().id,
                      tags=[tag1, tag2, tag3])
        db.session.add(new_job)
        db.session.commit()
        assert len(new_job.tags) == 3

    def test_add_categories(self):
        cat1 = Category.get_or_create(name='Educator')
        cat2 = Category.get_or_create(name='Analyst')
        cat3 = Category.get_or_create(name='Cartographer')
        new_job = Job(user_id=User.query.filter_by(email=self.admin_user).first().id,
                      categories=[cat1, cat2, cat3])
        db.session.add(new_job)
        db.session.commit()
        assert len(new_job.categories) == 3
