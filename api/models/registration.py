from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery

class RegistrationQuery(BaseQuery):

    def get_by_id(self, id):
        return self.filter(Registration.id == id).order_by(Registration.id.desc()).first()

    def get_by_phone(self, phone):
        return self.filter(Registration.user_phone == phone).first()

    def get_latest_by_phone(self, phone):
        return self.filter(Registration.user_phone == phone).order_by(Registration.id.desc()).first()

class Registration(TimestampMixin, db.Model):
    query_class = RegistrationQuery
    __tablename__ = 'registration'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_phone = db.Column(db.String(50), nullable=False)
    system_phone = db.Column(db.String(50), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    parent_type = db.Column(db.String(50))
    is_child_between_0_3 = db.Column(db.Boolean)
    is_child_between_3_6 = db.Column(db.Boolean)
    is_child_above_6 = db.Column(db.Boolean)
    has_no_child = db.Column(db.Boolean)
    has_smartphone = db.Column(db.Boolean)
    has_dropped_missedcall = db.Column(db.Boolean)
    has_received_callback = db.Column(db.Boolean)
    status = db.Column(db.String(50))
    signup_date = db.Column(db.DateTime)
