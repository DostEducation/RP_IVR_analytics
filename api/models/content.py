from api.mixins import TimestampMixin
from api import db


class Content(TimestampMixin, db.Model):
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50))
