from api.mixins import TimestampMixin
from api import db


class Module(TimestampMixin, db.Model):
    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
