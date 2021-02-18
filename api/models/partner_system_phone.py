from api.mixins import TimestampMixin
from api import db

class PartnerSystemPhone(TimestampMixin, db.Model):
    __tablename__ = 'partner_system_phone'
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    system_phone_id = db.Column(db.Integer, db.ForeignKey('system_phone.id'))
    status = db.Column(db.String(50))
