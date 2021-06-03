from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class UserQuery(BaseQuery):
    def get_by_phone(self, phone):
        return self.filter(User.phone == phone).first()

    def get_by_id(self, id):
        return self.filter(User.id == id).first()


class User(TimestampMixin, db.Model):
    query_class = UserQuery
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address_line_1 = db.Column(db.String(500))
    address_line_2 = db.Column(db.String(500))
    postal_code = db.Column(db.String(50))
    partner_id = db.Column(db.Integer, db.ForeignKey("partner.id"))
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(50))

    @classmethod
    def get_by_user_id(self, user_id):
        return User.query.get_by_id(user_id)
