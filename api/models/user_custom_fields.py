from api.mixins import TimestampMixin
from api import db, helpers
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc, and_


class UserCustomFieldsQuery(BaseQuery):
    def get_by_user_phone(self, phone):
        return self.filter(UserCustomFields.user_phone == phone).all()


class UserCustomFields(TimestampMixin, db.Model):
    query_class = UserCustomFieldsQuery
    __tablename__ = "user_custom_fields"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    registration_id = db.Column(db.Integer, db.ForeignKey("registration.id"))
    user_phone = db.Column(db.String(50), nullable=False)
    flow_run_uuid = db.Column(db.String(255))
    field_name = db.Column(db.String(255), nullable=False)
    field_value = db.Column(db.String(500), nullable=False)
