from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config.from_object('config.Config')
app.config.from_object('config')

db = SQLAlchemy(app)
from api import models
from api import views


# Need to remove this, keeping it till initial development
# db.create_all()
