from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

# Accessing the underlying engine and connection details
engine = db.engine
connection_url = str(engine.url)

print(f"The application is using the following database connection: {connection_url}")
