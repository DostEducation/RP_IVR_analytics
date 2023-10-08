from __future__ import absolute_import
from api import db, app
from api.models import *
from utils.loggingutils import logger


from flask_migrate import Migrate
from flask_script import Manager
from sqlalchemy import create_engine

migrate = Migrate(app, db)

manager = Manager(app)

if __name__ == "__main__":
    manager.run()

SQLALCHEMY_DATABASE_URI = app.config["SQLALCHEMY_DATABASE_URI"]


def select_user_phone_from_db(connection, cursor):
    try:
        cursor.executemany("SELECT phone FROM users")
        connection.commit()
    except Exception as e:
        connection.rollback()
        logger.error(f"Error occured while fetching data. Error Message: {e}")


try:
    # Create a SQLAlchemy engine using the database URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    # Attempt to establish a connection to the database
    connection = engine.connect()
    cursor = connection.cursor()

    # If the connection was successful, print a success message
    logger.info(f"Database connection successful on URI {SQLALCHEMY_DATABASE_URI}")
    user_data = select_user_phone_from_db(connection, cursor)
    logger.info(f"user data: {user_data}")

    # Close the connection
    connection.close()

except Exception as e:
    # Handle any exceptions that may occur during the connection attempt
    logger.error(f"Error connecting to the database: {str(e)}")
