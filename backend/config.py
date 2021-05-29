import os


class BaseConfig(object):
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # map settings for admin
    MAPBOX_MAP_ID = 'light-v10'
    MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN')
    DEFAULT_CENTER_LAT = -33.918861
    DEFAULT_CENTER_LONG = 18.423300

    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('JOBS_DATABASE_URL')
    SQLALCHEMY_BINDS = {
        'geonames': os.environ.get('GEONAMES_DATABASE_URL')
    }
    """Development configuration"""
    DEBUG_TB_ENABLED = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('JOBS_DATABASE_TEST_URL')
    SQLALCHEMY_BINDS = {
        'geonames': os.environ.get('GEONAMES_DATABASE_URL')
    }
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3


class StagingConfig(BaseConfig):
    """Staging configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('JOBS_DATABASE_URL')
    SQLALCHEMY_BINDS = {
        'geonames': os.environ.get('GEONAMES_DATABASE_URL')
    }


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('JOBS_DATABASE_URL')
    SQLALCHEMY_BINDS = {
        'geonames': os.environ.get('GEONAMES_DATABASE_URL')
    }
