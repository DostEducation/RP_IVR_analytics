from api.mixins import TimestampMixin
from api import db, helpers
from flask_sqlalchemy import BaseQuery


class UserGroupQuery(BaseQuery):
    def get_by_uuid(self, uuid):
        return self.filter(UserGroup.group_uuid == uuid).first()


class UserGroup(TimestampMixin, db.Model):
    query_class = UserGroupQuery
    __tablename__ = "user_group"
    id = db.Column(db.Integer, primary_key=True)
    user_phone = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    registration_id = db.Column(db.Integer, db.ForeignKey("registration.id"))
    group_name = db.Column(db.String(255), nullable=False)
    group_uuid = db.Column(db.String(255))
    status = db.Column(db.String(100))
