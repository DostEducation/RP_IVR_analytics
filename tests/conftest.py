import os
import pytest
from flask_sqlalchemy import SQLAlchemy
from api import app as flask_app
from migrations.seeders import testing_seeder


def is_testing_server():
    if os.environ["FLASK_ENV"] != "testing":
        return False
    return True


@pytest.fixture()
def app():
    if not is_testing_server():
        quit(
            "This is not a testing environment. Please run the tests from the test server."
        )
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db():
    db = SQLAlchemy(flask_app)
    db.init_app(flask_app)

    return db


@pytest.fixture(scope="session")
def setup_test_environment(db):
    # Creating tables.
    try:
        os.system("flask db downgrade 31955a9b7348")
        os.system("flask db downgrade")
        os.system("flask db upgrade")
    except Exception as e:
        raise e
        # os.system("flask db upgrade")

    # Loading pre-filled data for running tests.
    try:
        testing_seeder.main()
    except:
        db.session.rollback()
