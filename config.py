"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = environ.get('TESTING')
DEBUG = environ.get('DEBUG')
FLASK_ENV = environ.get('FLASK_ENV')

# Database configuration
POSTGRES = {
    'user': environ.get('DB_USER'),
    'password': environ.get('DB_PASSWORD'),
    'database': environ.get('DB_NAME'),
    'host': environ.get('DB_HOST'),
    'port': environ.get('DB_PORT'),
    'connection_name': environ.get('CONNECTION_NAME'),
}
# For socket based connection
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s/%(database)s?host=/cloudsql/%(connection_name)s/'  % POSTGRES
if FLASK_ENV == 'development':
	SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % POSTGRES


SQLALCHEMY_TRACK_MODIFICATIONS = True
WTF_CSRF_ENABLED = True
SECRET_KEY = environ.get('SECRET_KEY')
