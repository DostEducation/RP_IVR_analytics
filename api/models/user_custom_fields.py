from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery
from sqlalchemy import and_


class UserCustomFieldsQuery(BaseQuery):
    def get_by_user_phone(self, phone):
        return self.filter(UserCustomFields.user_phone == phone).all()

    def set_custom_field_as_inactive(self, phone, field_name, field_value):
        self.filter(
            and_(
                UserCustomFields.user_phone == phone,
                UserCustomFields.field_name == field_name,
                UserCustomFields.field_value == field_value,
            )
        ).update(
            {UserCustomFields.status: UserCustomFields.UserCustomFieldStatus.INACTIVE}
        )

    def set_custom_field_as_active(self, field_name, field_value, phone):
        self.filter(
            and_(
                UserCustomFields.user_phone == phone,
                UserCustomFields.field_name == field_name,
                UserCustomFields.field_value == field_value,
            )
        ).update(
            {UserCustomFields.status: UserCustomFields.UserCustomFieldStatus.ACTIVE}
        )


class UserCustomFields(TimestampMixin, db.Model):
    query_class = UserCustomFieldsQuery
    __tablename__ = "user_custom_fields"

    class UserCustomFieldStatus:
        ACTIVE = "active"
        INACTIVE = "inactive"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    registration_id = db.Column(db.Integer, db.ForeignKey("registration.id"))
    user_phone = db.Column(db.String(50), nullable=False)
    flow_run_uuid = db.Column(db.String(255))
    field_name = db.Column(db.String(255), nullable=False)
    field_value = db.Column(db.String(500), nullable=False)
    status = db.Column(
        db.String(100), nullable=False, default=UserCustomFieldStatus.INACTIVE
    )
