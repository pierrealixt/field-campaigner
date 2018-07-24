import os

# import SECRET_KEY into current namespace
# noinspection PyUnresolvedReferences

try:
    from secret import SECRET_KEY as THE_SECRET_KEY  # noqa
    from secret import OAUTH_CONSUMER_KEY, OAUTH_SECRET, SENTRY_DSN
except ImportError:
    THE_SECRET_KEY = os.environ['SECRET_KEY']

    if 'OAUTH_CONSUMER_KEY' in os.environ:
        OAUTH_CONSUMER_KEY = os.environ['OAUTH_CONSUMER_KEY']
    else:
        OAUTH_CONSUMER_KEY = 'SET_OAUTH_CONSUMER_KEY'

    if 'OAUTH_SECRET' in os.environ:
        OAUTH_SECRET = os.environ['OAUTH_SECRET']
    else:
        OAUTH_SECRET = 'SET_OAUTH_SECRET'

    SENTRY_DSN = os.environ['SENTRY_DSN']


try:
    DATA_FOLDER = os.environ['DATA_FOLDER']
except KeyError:
    DATA_FOLDER = 'home/web/field-campaigner-data'


class Config(object):
    """Configuration environment for application.
    """
    # DEBUG = False
    # TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = THE_SECRET_KEY
    OAUTH_CONSUMER_KEY = OAUTH_CONSUMER_KEY
    OAUTH_SECRET = OAUTH_SECRET
    SENTRY_DSN = SENTRY_DSN
    MAX_AREA_SIZE = 320000000

    # OSMCHA ATTRIBUTES
    _OSMCHA_DOMAIN = 'https://osmcha.mapbox.com/'
    OSMCHA_API = _OSMCHA_DOMAIN + 'api/v1/'
    OSMCHA_FRONTEND_URL = 'https://osmcha.mapbox.com/'

    # CAMPAIGN DATA
    campaigner_data_folder = "./campaign_manager/static"


class ProductionConfig(Config):
    """Production environment.
    """
    DEBUG = False
    if 'DATABASE_URL' in os.environ:
        DB_LOCATION = os.environ['DATABASE_URL']


class StagingConfig(Config):
    """Staging environment.
    """
    DEVELOPMENT = True
    DEBUG = True
    if 'DATABASE_URL' in os.environ:
        DB_LOCATION = os.environ['DATABASE_URL']


class AWSStagingConfig(Config):
    DEBUG = False

    if 'RDS_USERNAME' in os.environ:
        DB_LOCATION = 'postgres://{}:{}@{}/{}'.format(
            os.environ['RDS_USERNAME'],
            os.environ['RDS_PASSWORD'],
            os.environ['RDS_HOSTNAME'],
            os.environ['RDS_DB_NAME'])


class AWSDevelopmentConfig(Config):
    """ AWS Development environment.
    """
    DEVELOPMENT = True
    DEBUG = True

    if 'RDS_USERNAME' in os.environ:
        DB_LOCATION = 'postgres://{}:{}@{}/{}'.format(
            os.environ['RDS_USERNAME'],
            os.environ['RDS_PASSWORD'],
            os.environ['RDS_HOSTNAME'],
            os.environ['RDS_DB_NAME'])


class DevelopmentConfig(Config):
    """Development environment.
    """
    DEVELOPMENT = True
    TESTING = False
    DEBUG = True
    if 'DATABASE_URL' in os.environ:
        DB_LOCATION = os.environ['DATABASE_URL']


class TestingConfig(Config):
    """Testing environment.
    """
    DEBUG = True
    TESTING = True
    DEVELOPMENT = False
    WTF_CSRF_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    if 'TESTDATABASE_URL' in os.environ:
        DB_LOCATION = os.environ['TESTDATABASE_URL']

    DRIVER_PATH = os.path.abspath('./campaign_manager/test/chromedriver')
