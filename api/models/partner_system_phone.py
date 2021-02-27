from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery

class PartnerSystemPhoneQuery(BaseQuery):

    def get_by_system_phone_id(self, system_phone):
        return self.filter(PartnerSystemPhone.system_phone == system_phone).first()

class PartnerSystemPhone(TimestampMixin, db.Model):
	query_class = PartnerSystemPhoneQuery
	__tablename__ = 'partner_system_phone'
	id = db.Column(db.Integer, primary_key=True)
	partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
	system_phone_id = db.Column(db.Integer, db.ForeignKey('system_phone.id'))
	status = db.Column(db.String(50))
