from api.mixins import TimestampMixin
from api import db


class Program(TimestampMixin, db.Model):
    __tablename__ = "program"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(500))
    start_date = db.Column(db.Date, nullable=False)
    discontinuation_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    program_type = db.Column(db.String(50))
