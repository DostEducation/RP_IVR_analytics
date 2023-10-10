from __future__ import absolute_import
from api import db, app
from api.models import *
from utils.loggingutils import logger

from flask_migrate import Migrate
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)

if __name__ == "__main__":
    manager.run()

SQLALCHEMY_DATABASE_URI = app.config["SQLALCHEMY_DATABASE_URI"]

from sqlalchemy import create_engine, text

try:
    # Create a SQLAlchemy engine using the database URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    # Attempt to establish a connection to the database
    connection = engine.connect()

    # If the connection was successful, print a success message
    logger.info(f"Database connection successful on URI {SQLALCHEMY_DATABASE_URI}")

    # Use SQLAlchemy's text function to create an SQL statement
    sql_statement = text("CREATE TABLE users (phone VARCHAR)")

    # Execute the SQL statement
    connection.execute(sql_statement)

    # Use SQLAlchemy's text function to create an SQL statement
    sql_statement = text("INSERT INTO users (phone) VALUES ('1234567890')")

    # Execute the SQL statement
    connection.execute(sql_statement)
    # Use SQLAlchemy's text function to create an SQL statement
    sql_statement = text("SELECT phone FROM users")

    result = connection.execute(sql_statement)

    # Fetch all the rows from the result set
    user_data = result.fetchall()
    logger.info(f"user data: {user_data}")

    # Close the connection
    connection.close()

except Exception as e:
    # Handle any exceptions that may occur during the connection attempt
    logger.error(f"Error connecting to the database: {str(e)}")
