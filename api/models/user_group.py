from api.mixins import TimestampMixin
from api import db, helpers
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc, and_


class UserGroupQuery(BaseQuery):
    def get_by_uuid(self, uuid):
        return self.filter(UserGroup.group_uuid == uuid).first()

    def get_by_user_phone(self, phone):
        return self.filter(UserGroup.user_phone == phone).all()

    def get_unique(self, uuid, phone):
        return (
            self.filter(
                and_(
                    UserGroup.group_uuid == uuid,
                    UserGroup.user_phone == phone,
                )
            )
            .order_by(desc(UserGroup.created_on))
            .first()
        )

    def mark_user_groups_as_inactive(self, phone, uuid):
        self.filter(
            and_(UserGroup.user_phone == phone, UserGroup.group_uuid == uuid)
        ).update({UserGroup.status: UserGroup.UserGroupStatus.INACTIVE})


class UserGroup(TimestampMixin, db.Model):
    query_class = UserGroupQuery
    __tablename__ = "user_group"

    class UserGroupStatus(object):
        ACTIVE = "active"
        INACTIVE = "inactive"

    id = db.Column(db.Integer, primary_key=True)
    user_phone = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    registration_id = db.Column(db.Integer, db.ForeignKey("registration.id"))
    group_name = db.Column(db.String(255), nullable=False)
    group_uuid = db.Column(db.String(255))
    status = db.Column(db.String(100))
