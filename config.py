"""Flask configuration."""
import os
from common_utils import CommonUtils

FLASK_ENV = os.environ.get("FLASK_ENV", "development")

if FLASK_ENV == "development":
    from os import path
    from dotenv import load_dotenv

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, ".env"))

TESTING = os.environ.get("TESTING")
DEBUG = os.environ.get("DEBUG")
SERVER_TYPE = os.environ.get("SERVER_TYPE")

# Database configuration
DB_NAME = CommonUtils.get_env_sensative_variable("DB_NAME")
DB_USER = CommonUtils.get_env_sensative_variable("DB_USER")
DB_HOST = CommonUtils.get_env_sensative_variable("DB_HOST")
DB_PWD = CommonUtils.get_env_sensative_variable("DB_PASSWORD")
DB_PORT = CommonUtils.get_env_sensative_variable("DB_PORT")
POSTGRES = {
    "user": DB_USER,
    "password": DB_PWD,
    "database": DB_NAME,
    "host": DB_HOST,
    "port": DB_PORT,
    "connection_name": os.environ.get("CONNECTION_NAME"),
}

SQLALCHEMY_DATABASE_URI = (
    "postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % POSTGRES
)

# For socket based connection
if FLASK_ENV == "staging":
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://%(user)s:%(password)s@/%(database)s?host=%(connection_name)s/"
        % POSTGRES
    )

github_action_db_url = os.environ.get("SQLALCHEMY_DATABASE_URI_GITHUB_ACTION", None)

if github_action_db_url:
    SQLALCHEMY_DATABASE_URI = github_action_db_url

SQLALCHEMY_TRACK_MODIFICATIONS = True
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")

DEFAULT_PROGRAM_ID = 2
DEFAULT_LANGUAGE_ID = 1
DEFAULT_PROGRAM_TIME_CATEGORY = "AFTERNOON"
RETRY_LOGS_BATCH_LIMIT = os.environ.get("RETRY_LOGS_BATCH_LIMIT", 1000)
MAX_RETRY_ATTEMPTS_FOR_LOGS = os.environ.get("MAX_RETRY_ATTEMPTS_FOR_LOGS", 3)
