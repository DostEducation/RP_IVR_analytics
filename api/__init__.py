from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

print("DATABASE_URL:", app.config["SQLALCHEMY_DATABASE_URI"])
