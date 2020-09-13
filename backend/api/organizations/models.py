from datetime import datetime
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import func, event
from slugify import slugify
from sqlalchemy.ext.declarative import declared_attr

from api import db
from api.utils import dump_geo, dump_datetime, get_slug
from api.geonames.models import WorldBorders

organization_jobs = db.Table('organization_jobs',
                             db.Column('organization_id', db.Integer, db.ForeignKey('organization.id'),
                                       primary_key=True),
                             db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True)
                             )

job_tags = db.Table('organization_tags',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                    db.Column('organization_id', db.Integer, db.ForeignKey('organization.id'), primary_key=True)
                    )


class BaseMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Organization(db.Model):
    __table_args__ = (
        db.Index('idx_organization_geom', 'the_geom', postgresql_using='gist'),
        db.Index('idx_organization_slug', 'slug'),
        db.Index('idx_organization_name', 'name'),
        db.Index('idx_organization_sector', 'sector'),
        db.Index('idx_organization_user_id', 'user_id'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    slug = db.Column(db.String(150))

    name = db.Column(db.String(100))
    headline = db.Column(db.String(160))
    year_founded = db.Column(db.String(4))
    size = db.Column(db.String(20))
    logo = db.Column(db.String)
    url = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    sector = db.Column(db.String(10))  # public, private, non-profit
    # industry = db.Column(db.String(50))

    contact_name = db.Column(db.String(50))
    contact_phone = db.Column(db.String(50))
    contact_email = db.Column(db.String(100))

    # admin
    clicks = db.Column(db.Integer, default=0)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow())
    edit_date = db.Column(db.DateTime, default=None)
    is_active = db.Column(db.Boolean, default=True)
    is_sponsor = db.Column(db.Boolean, default=False)
    data_source = db.Column(db.String(10), default='indeed')

    # location
    hires_remote = db.Column(db.Boolean)
    is_distributed = db.Column(db.Boolean, default=False)
    street_address = db.Column(db.String(75))
    postal_code = db.Column(db.String(10))
    city = db.Column(db.String(75))
    state = db.Column(db.String(50))
    formatted_location = db.Column(db.String(125))
    country_code = db.Column(db.String(3))
    invalid_geom = db.Column(db.Boolean, default=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    the_geom = db.Column(Geometry('POINT', 4326, spatial_index=False))

    users = db.relationship("User")
    jobs = db.relationship('Job', secondary=organization_jobs, lazy='subquery',
                           backref=db.backref('organizations', lazy=True))

    tags = db.relationship('Tag', secondary=job_tags, lazy='subquery',
                           backref=db.backref('organizations', lazy=True))

    def __init__(self, **kwargs):
        super(Organization, self).__init__(**kwargs)
        if self.name:
            self.name = self.name[:100]
        if self.city:
            self.city = self.city[:75]
        if self.state:
            self.state = self.state[:50]
        if self.formatted_location:
            self.formatted_location = self.formatted_location[:125]
        elif self.city and self.state:
            self.formatted_location = "{}, {}".format(self.city[:75], self.state[:75])
        if self.country_code:
            self.country_code = self.country_code.lower()
        if self.description:
            self.description = self.description.replace("\"", "'")[:1000]
        if self.name:
            self.slug = slugify(self.name, max_length=100)
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
        elif not self.is_distributed:
            self.invalid_geom = True

    @classmethod
    def on_update(cls, **kw):
        obj = db.session.query(cls).filter(cls.id == kw['id']).first()
        if obj.name:
            obj.slug = slugify(obj.name, max_length=100)
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
        elif not obj.is_distributed:
            obj.invalid_geom = True
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def query_from_slug(cls, slug):
        if len(slug):
            return db.session.query(cls).filter(cls.id == slug.split("-")[0]).first()
        return None

    @classmethod
    def bbox(cls, coords):
        return db.session.query(cls).filter(cls.the_geom.ST_Envelope(coords)).filter(cls.is_active).all()

    @property
    def serialize_preview(self):
        """Return object data in easily serializeable format"""
        return {
            "type": "Feature",
            "properties": {
                'name': self.name,
                'headline': self.headline,
                'logo': self.logo,
                'slug': get_slug(self.id, self.slug),
                'isSponsor': self.is_sponsor,
                'isDistributed': self.is_distributed,
                'formattedLocation': self.formatted_location
            },
            'geometry': dump_geo(self.the_geom),
        }

    @property
    def serialize_org(self):
        """Return object data in easily serializeable format"""
        return {
            "type": "Feature",
            "properties": {
                # 'id': self.id,
                'name': self.name,
                'formattedLocation': self.formatted_location,
                'description': self.description,
                'slug': get_slug(self.id, self.slug),
                'publishDate': dump_datetime(self.publish_date),
                'hiresRemote': self.hires_remote,
                'contactEmail': self.contact_email,
                'contactPhone': self.contact_phone,
                'contactName': self.contact_name
            },
            'geometry': dump_geo(self.the_geom),
        }


# class OrganizationLocation(db.Model):
#     __table_args__ = (
#         db.Index('idx_organizationloc_geom', 'the_geom', postgresql_using='gist'),
#     )
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
#
#     # location
#     city = db.Column(db.String(150))
#     state = db.Column(db.String(150))
#     postal_code = db.Column(db.String(50))
#     country_code = db.Column(db.String(3))
#     location_formatted = db.Column(db.String(250))
#     invalid_geom = db.Column(db.Boolean, default=False)
#     description = db.Column(db.String(500))
#     lat = db.Column(db.Float)
#     lon = db.Column(db.Float)
#     the_geom = db.Column(Geometry('POINT', 4326, spatial_index=True))
#
#     @classmethod
#     def bbox(cls, coords):
#         return db.session.query(cls).filter(cls.the_geom.ST_Envelope(coords)).all()
#
#     def __init__(self, **kwargs):
#         super(Organization, self).__init__(**kwargs)
#
#         if self.lon == 0 and self.lat == 0:
#             self.invalid_geom = True
#         elif self.country_code and self.lon and self.lat:
#             # create geometry and determine if valid
#             self.the_geom = WKTElement('POINT({0} {1})'.format(self.lon, self.lat), srid=4326)
#             q = db.session.query(WorldBorders) \
#                 .filter(WorldBorders.iso2 == self.country_code.upper(),
#                         func.ST_DWithin(WorldBorders.geom, self.the_geom, 5)).first()
#             if q:
#                 self.invalid_geom = False
#             else:
#                 self.invalid_geom = True
#         else:
#             self.invalid_geom = True
#
#     @property
#     def serialize_preview(self):
#         """Return object data in easily serializeable format"""
#         return {
#             "type": "Feature",
#             "properties": {
#                 'id': self.id,
#                 'name': self.name,
#                 'city': self.city,
#                 'state': self.state,
#                 'slug': self.slug,
#                 'organization': Organization(id=self.id).serialize_preview,
#             },
#             'geometry': dump_geo(self.the_geom.data),
#         }
