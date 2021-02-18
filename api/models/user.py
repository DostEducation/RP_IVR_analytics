
from api.mixins import TimestampMixin
from api import db

class User(TimestampMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address_line_1 = db.Column(db.String(500))
    address_line_2 = db.Column(db.String(500))
    postal_code = db.Column(db.String(50))
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(50))
