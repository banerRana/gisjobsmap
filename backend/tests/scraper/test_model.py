from api import db
from api.scraper.models import Invalid, Status
from tests.base import BaseTestCase
from datetime import datetime
import time


class TestInvalidModel(BaseTestCase):

    def test_invalid_bulk_add(self):
        invalid_keys = ['123456780', '123456781', '123456782', '123456783', '123456784', '123456785', '123456786']
        Invalid.bulk_add(keys=invalid_keys)
        results = db.session.query(Invalid).all()
        self.assertEqual(len(results), len(invalid_keys))

    def test_invalid_prune(self):
        invalid_keys = ['123456780', '123456781', '123456782', '123456783', '123456784', '123456785', '123456786']
        Invalid.bulk_add(keys=invalid_keys)
        Invalid.prune()
        results = db.session.query(Invalid).all()
        self.assertEqual(len(results), len(invalid_keys))

    def test_status_insert(self):
        start_time = datetime.utcnow()
        time.sleep(1)
        new_status = Status(
            time_start=start_time,
            is_success=True,
            errors=0,
            messages="message 1;message 2;",
            new=100,
            total_valid=2000,
            processed=5000,
            expired=300,
        )
        db.session.add(new_status)
        db.session.commit()
        assert new_status.time_end > new_status.time_start
        assert new_status.run_time is not None

    def test_status_prune(self):
        new_status = Status(
            time_start= datetime.utcnow(),
            is_success=True,
            errors=0,
            messages="message 1;message 2;",
            new=100,
            total_valid=2000,
            processed=5000,
            expired=300,
        )
        db.session.add(new_status)
        db.session.commit()
        Status.prune()
        results = db.session.query(Status).all()
        self.assertEqual(len(results), 1)
