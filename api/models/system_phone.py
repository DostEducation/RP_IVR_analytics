from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy.query import Query as BaseQuery


class SystemPhoneQuery(BaseQuery):
    def get_by_phone(self, phone):
        return self.filter(SystemPhone.phone.contains(phone[-10:])).first()

    def get_by_id(self, system_phone_id):
        return self.filter(SystemPhone.id == system_phone_id).first()


class SystemPhone(TimestampMixin, db.Model):
    query_class = SystemPhoneQuery
    __tablename__ = "system_phone"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    status = db.Column(db.String(50))
