from api.auth.models import User
from api import db
from tests.base import BaseTestCase


class TestJobBase(BaseTestCase):

    def setUp(self):
        db.create_all(bind=None)
        db.session.commit()
        admin_user = User(email=self.admin_user,
                          password=self.admin_pass,
                          confirmed=True,
                          admin=True)
        db.session.add(admin_user)
        user = User(email=self.reg_user,
                    password=self.reg_pass,
                    confirmed=True,
                    admin=False)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all(bind=None)
