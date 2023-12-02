import os
import pytest
from flask_sqlalchemy import SQLAlchemy
from api import app as flask_app


def is_testing_server():
    if flask_app.config["SERVER_TYPE"] != "test":
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
    try:
        os.system("flask db downgrade f4c3bfdad519")
        os.system("flask db downgrade")
        os.system("flask db upgrade")
    except:
        os.system("flask db upgrade")

    # testing_seeder.main()
