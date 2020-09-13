from datetime import datetime, timedelta

import jwt
from api import db, bcrypt
from api.geonames.models import WorldBorders
from flask import current_app
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import func


# simple analytics
class UserLocation(db.Model):
    __tablename__ = 'user_location'
    __table_args__ = (
        db.Index('idx_user_geom', 'the_geom', postgresql_using='gist'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow())
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    iso_2 = db.Column(db.String)
    city = db.Column(db.String)
    country_name = db.Column(db.String)
    the_geom = db.Column(Geometry('POINT', 4326, spatial_index=False))

    def __repr__(self):
        return '<UserLocation {}>'.format(self.city)

    def __init__(self, **kwargs):
        super(UserLocation, self).__init__(**kwargs)

        if self.lon == 0 and self.lat == 0:
            self.invalid_geom = True
        elif self.iso_2 and self.lon and self.lat:
            # create geometry and determine if valid
            self.the_geom = WKTElement('POINT({0} {1})'.format(self.lon, self.lat), srid=4326)
            q = db.session.query(WorldBorders) \
                .filter(WorldBorders.iso2 == self.iso_2.upper(),
                        func.ST_DWithin(WorldBorders.geom, self.the_geom, 5)).first()
            if q:
                self.invalid_geom = False
            else:
                self.invalid_geom = True
        else:
            self.invalid_geom = True


class User(db.Model):
    __table_args__ = (
        db.Index('idx_user_email', 'email'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password, confirmed=False, admin=False, confirmed_on=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.utcnow()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'active': self.active,
            'admin': self.admin
        }

    def encode_auth_token(self, user_id):
        """Generates the auth token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token - :param auth_token: - :return: integer|string
        """
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'), algorithms='HS256')
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.utcnow()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class Searches(db.Model):
    '''
    saved User searches
    '''
    __tablename__ = 'searches'
    __table_args__ = (
        db.Index('idx_searches_geom', 'the_geom', postgresql_using='gist'),
    )
    """ For job seekers to search on geometry"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    term = db.Column(db.String)
    user_emailed = db.Column(db.Boolean, default=False)
    user_account = db.relationship("User")
    the_geom = db.Column(Geometry('POLYGON', 4326, spatial_index=False))

    def __repr__(self):
        return '<Searches %r>' % self.id
