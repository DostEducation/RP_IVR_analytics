from __future__ import absolute_import
from api import db, app

from flask_migrate import Migrate
from flask.cli import FlaskGroup

migrate = Migrate(app, db)
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
