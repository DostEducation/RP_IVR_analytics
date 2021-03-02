"""Flask configuration."""
from os import environ, path
# from dotenv import load_dotenv

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

TESTING = environ.get('TESTING')
DEBUG = environ.get('DEBUG')
FLASK_ENV = environ.get('FLASK_ENV')

# Database configuration #
# [database]

POSTGRES = {
    'user': environ.get('DB_USER'),
    'password': environ.get('DB_PASSWORD'),
    'database': environ.get('DB_NAME'),
    'host': environ.get('DB_HOST'),
    'port': environ.get('DB_PORT'),
}

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % POSTGRES

WTF_CSRF_ENABLED = True
SECRET_KEY = environ.get('SECRET_KEY')
