from __future__ import absolute_import
from api import db, app
from api.models import *
from utils.loggingutils import logger


from flask_migrate import Migrate
from flask_script import Manager
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

migrate = Migrate(app, db)

manager = Manager(app)

if __name__ == "__main__":
    manager.run()

SQLALCHEMY_DATABASE_URI = app.config["SQLALCHEMY_DATABASE_URI"]

try:
    # Create a SQLAlchemy engine using the database URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    # Attempt to establish a connection to the database
    connection = engine.connect()

    # If the connection was successful, print a success message
    logger.warning("Database connection successful!")

    # Close the connection
    connection.close()

except OperationalError as e:
    # Handle any exceptions that may occur during the connection attempt
    logger.error(f"Error connecting to the database: {str(e)}")
