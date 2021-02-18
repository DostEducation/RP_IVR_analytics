from api.mixins import TimestampMixin
from api import db

class SystemPhone(TimestampMixin, db.Model):
    __tablename__ = 'system_phone'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    status = db.Column(db.String(50))