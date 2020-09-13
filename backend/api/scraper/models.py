from api import db
from datetime import datetime, timedelta


class Invalid(db.Model):
    __tablename__ = 'invalid'
    __table_args__ = (
        db.Index('idx_invalid_key', 'key'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(16), unique=True)
    scrape_date = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def bulk_add(cls, keys):
        if keys:
            objects = []
            for k in keys:
                objects.append(cls(key=k))
            db.session.bulk_save_objects(objects)
            db.session.commit()

    @classmethod
    def prune(cls):
        days = datetime.today() - timedelta(days=240)
        db.session.query(cls).filter(cls.scrape_date < days).delete()
        db.session.commit()

    def __repr__(self):
        return '<Invalid key {}>'.format(self.key)


class Status(db.Model):
    __tablename__ = 'scraper_status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_start = db.Column(db.DateTime, default=None)
    time_end = db.Column(db.DateTime, default=None)
    run_time = db.Column(db.Interval, default=None)
    is_success = db.Column(db.Boolean)
    errors = db.Column(db.Integer, default=0)
    messages = db.Column(db.String, default='')
    new = db.Column(db.Integer, default=0)
    total_valid = db.Column(db.Integer, default=0)
    processed = db.Column(db.Integer, default=0)
    expired = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Status, self).__init__(**kwargs)
        if self.time_start:
            if type(self.time_start) == str:
                self.time_start = datetime.strptime(self.time_start, '%Y-%m-%d %H:%M:%S.%f').replace(microsecond=0)
            else:
                self.time_start = self.time_start.replace(microsecond=0)
            self.time_end = datetime.utcnow().replace(microsecond=0)
            self.run_time = datetime.utcnow() - self.time_start

    def __repr__(self):
        return '<Status status {}>'.format(self.status)

    @classmethod
    def prune(cls):
        days = datetime.today() - timedelta(days=90)
        db.session.query(cls).filter(cls.time_start < days).delete()
        db.session.commit()
