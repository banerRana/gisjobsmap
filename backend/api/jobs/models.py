from datetime import datetime

from api import db
from api.geonames.models import WorldBorders
from api.utils import dump_geo, dump_datetime
from geoalchemy2 import Geometry, WKTElement
from slugify import slugify
from sqlalchemy import func

job_tags = db.Table('job_tags',
                    db.metadata,
                    db.Column("id", db.Integer, primary_key=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
                    )
db.Index("tag_search", job_tags.c.job_id, job_tags.c.tag_id, unique=True)

job_categories = db.Table('job_categories',
                          db.metadata,
                          db.Column("id", db.Integer, primary_key=True),
                          db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                          db.Column('job_id', db.Integer, db.ForeignKey('job.id'))
                          )
db.Index("category_search", job_categories.c.job_id, job_categories.c.category_id, unique=True)


class Job(db.Model):
    __table_args__ = (
        db.Index('idx_jobs_geom', 'the_geom', postgresql_using='gist'),
        db.Index('idx_jobs_indeed_key', 'indeed_key'),
        db.Index('idx_jobs_source', 'data_source'),
        db.Index('idx_jobs_user_id', 'user_id'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    indeed_key = db.Column(db.String(25), unique=True, default=None)
    indeed_search_term = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    logo = db.Column(db.String)
    company = db.Column(db.String(100))
    url = db.Column(db.String)

    contact_name = db.Column(db.String(50))
    contact_phone = db.Column(db.String(50))
    contact_email = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_remote = db.Column(db.Boolean)
    employment_type = db.Column(db.String(50))  # full time, part time, contract, etc..
    career_level = db.Column(db.String(100))
    compensation = db.Column(db.String(150))
    travel_percentage = db.Column(db.Integer)
    security_clearance_req = db.Column(db.Boolean)
    security_type = db.Column(db.String(100))

    # admin
    # clicks = db.Column(db.Integer, default=0)
    publish_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    expire_date = db.Column(db.DateTime(timezone=True), default=None)
    edit_date = db.Column(db.DateTime(timezone=True), default=None)
    is_active = db.Column(db.Boolean, default=True)
    social_network_shared = db.Column(db.Boolean, default=False)
    data_source = db.Column(db.String(10))

    # location
    city = db.Column(db.String(75))
    state = db.Column(db.String(50))
    formatted_location = db.Column(db.String(125))
    country_code = db.Column(db.String(3))
    invalid_geom = db.Column(db.Boolean, default=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    the_geom = db.Column(Geometry('POINT', 4326, spatial_index=False))
    users = db.relationship("User")
    tags = db.relationship('Tag', secondary=job_tags,
                           backref=db.backref('jobs', lazy='dynamic'))

    categories = db.relationship('Category', secondary=job_categories,
                                 backref=db.backref('jobs', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Job, self).__init__(**kwargs)
        if not self.data_source:
            self.data_source = 'gjm'
        if self.company:
            self.company = self.company[:100]
        if self.title:
            self.title = self.title[:100]
        if self.city:
            self.city = self.city[:75]
        if self.state:
            self.state = self.state[:50]
        if self.formatted_location:
            self.formatted_location = self.formatted_location[:125]
        elif self.city and self.state:
            self.formatted_location = "{}, {}".format(self.city[:75], self.state[:75])
        if self.description:
            self.description = self.description.replace("\"", "'")
        if self.country_code:
            self.country_code = self.country_code.lower()
        if self.title:
            self.slug = slugify(self.title, max_length=100)
        if self.lat:
            self.lat = float(self.lat)
        if self.lon:
            self.lon = float(self.lon)
        if self.country_code and self.lon and self.lat:
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

    @classmethod
    def on_update(cls, **kw):
        obj = db.session.query(cls).filter(cls.id == kw['id']).first()
        if obj.title:
            obj.slug = slugify(obj.title, max_length=100)
        if obj.country_code and obj.lon and obj.lat:
            # create geometry and determine if valid
            obj.the_geom = WKTElement('POINT({0} {1})'.format(obj.lon, obj.lat), srid=4326)
            q = db.session.query(WorldBorders) \
                .filter(WorldBorders.iso2 == obj.country_code.upper(),
                        func.ST_DWithin(WorldBorders.geom, obj.the_geom, 5)).first()
            if q:
                obj.invalid_geom = False
            else:
                obj.invalid_geom = True
        elif not obj.is_remote:
            obj.invalid_geom = True
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def bbox(cls, coords):
        return db.session.query(cls).filter(cls.the_geom.ST_Envelope(coords)).filter(cls.is_active).all()

    @classmethod
    def query_from_slug(cls, slug):
        if len(slug):
            return db.session.query(cls).filter(cls.id == slug.split("-")[0]).first()

    @property
    def link(self):
        return "{}-{}".format(self.id, self.slug)

    @property
    def serialize_preview(self):
        """Return object data in easily serializeable format"""
        return {
            "type": "Feature",
            "properties": {
                'title': self.title,
                'company': self.company,
                'formattedLocation': self.formatted_location,
                'countryCode': self.country_code,
                'dataSource': self.data_source,
                'slug': self.link,
                'publishDate': dump_datetime(self.publish_date),
                'isRemote': self.is_remote,
                'invalidGeom': self.invalid_geom,
                'categories': self.serialize_categories if self.data_source == 'gjm' else []
            },
            'geometry': dump_geo(self.the_geom),
        }

    @property
    def serialize_job(self):
        """Return object data in easily serializeable format"""
        return {
            "type": "Feature",
            "properties": {
                # 'id': self.id,
                'title': self.title,
                'company': self.company,
                'city': self.city,
                'state': self.state,
                'countryCode': self.country_code,
                'formattedLocation': self.formatted_location,
                'url': self.url,
                'slug': self.link,
                'description': self.description,
                'lastEdit': dump_datetime(self.edit_date),
                'publishDate': dump_datetime(self.publish_date),
                'isRemote': self.is_remote,
                'isActive': self.is_active,
                'dataSource': self.data_source,
                'invalidGeom': self.invalid_geom,
                'tags': self.serialize_tags,
                'categories': self.serialize_categories
            },
            'geometry': dump_geo(self.the_geom),
        }

    @property
    def serialize_tags(self):
        return [item.serialize for item in self.tags]

    @property
    def serialize_categories(self):
        return [item.serialize for item in self.categories]

    def __repr__(self):
        return '<Job {} - {}>'.format(self.id, self.title)
