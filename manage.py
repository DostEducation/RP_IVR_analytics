from __future__ import absolute_import
from api import db, app
from api.models import *


from flask_migrate import Migrate
from flask_script import Manager

migrate = Migrate(app, db)

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
