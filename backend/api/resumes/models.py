from api import db
from datetime import datetime
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import func
from slugify import slugify

from api.utils import dump_geo, dump_datetime
from api.geonames.models import WorldBorders

resume_tags = db.Table('resume_tags',
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                       db.Column('resume_id', db.Integer, db.ForeignKey('resume.id'), primary_key=True)
                       )

resume_categories = db.Table('resume_categories',
                         db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
                         db.Column('resume_id', db.Integer, db.ForeignKey('resume.id'), primary_key=True)
                         )


class Resume(db.Model):
    __table_args__ = (
        db.Index('idx_resume_geom', 'the_geom', postgresql_using='gist'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_account = db.relationship("User")

    slug = db.Column(db.String(150), index=True)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow())
    is_active = db.Column(db.Boolean, default=True)
    header = db.Column(db.String(100))
    description = db.Column(db.String(500))
    postgrad_degree=db.Column(db.String(100))
    grad_degree = db.Column(db.String(100))
    undergrad_degree = db.Column(db.String(100))
    other_education = db.Column(db.String(100))
    yrs_experience = db.Column(db.Integer)
    resume = db.Column(db.String)  # path to resume file

    relocation_ok = db.Column(db.Boolean)
    remote_ok = db.Column(db.Boolean)
    has_work_authorization = db.Column(db.Boolean)

    portfolio_url = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    stackexch_url = db.Column(db.String(255))

    # privacy
    is_public = db.Column(db.Boolean, default=True)

    # location
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    formattedlocation = db.Column(db.String(150))
    country_code = db.Column(db.String(3))
    the_geom = db.Column(Geometry('POINT', 4326, spatial_index=False))

    tags = db.relationship('Tag', secondary=resume_tags, lazy='subquery',
                           backref=db.backref('resumes', lazy=True))

    categories = db.relationship('Category', secondary=resume_categories, lazy='subquery',
                             backref=db.backref('resumes', lazy=True))

    def __repr__(self):
        return '<Resume %r>' % self.id

    @classmethod
    def bbox(cls, coords):
        return db.session.query(cls).filter(cls.the_geom.ST_Envelope(coords)).filter(cls.is_active == True).all()

    def __init__(self, **kwargs):
        super(Resume, self).__init__(**kwargs)

        # slugify - create unique URL friendly name
        text = "{}-{}".format(self.id, self.name)
        self.slug = slugify(text, max_length=150)

        if self.lon == 0 and self.lat == 0:
            self.invalid_geom = True
        elif self.country_code and self.lon and self.lat:
            # create geometry and determine if valid
            self.the_geom = WKTElement('POINT({0} {1})'.format(self.lon, self.lat), srid=4326)
            q = db.session.query(WorldBorders) \
                .filter(WorldBorders.iso2 == self.country_code.upper(),
                        func.ST_DWithin(WorldBorders.geom, self.the_geom, 5)).first()
            if q:
                self.invalid_geom = False
            else:
                self.invalid_geom = True
        else:
            self.invalid_geom = True

    @property
    def serialize_preview(self):
        """Return object data in easily serializeable format"""
        return {
            "type": "Feature",
            "properties": {
                'id': self.id,
                'name': self.name,
                'formattedLocation': self.formattedlocation,
                'slug': self.slug,
                'publishDate': dump_datetime(self.publish_date),
                'hiresRemote': self.hires_remote,
            },
            'geometry': dump_geo(self.the_geom.data),
        }

    @property
    def serialize_job(self):
        """Return object data in easily serializeable format"""
        return {
            "type": "Feature",
            "properties": {
                'id': self.id,
                'name': self.name,
                'formattedLocation': self.formattedlocation,
                'slug': self.slug,
                'publishDate': dump_datetime(self.publish_date),
                'hiresRemote': self.hires_remote,
                'contact': {'email':self.contact_email,
                            'phone': self.contact_phone,
                            'name': self.contact_name}
            },
            'geometry': dump_geo(self.the_geom.data),
        }