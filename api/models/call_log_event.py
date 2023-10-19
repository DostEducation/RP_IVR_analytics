from api.mixins import TimestampMixin
from api import db


class CallLogEvent(TimestampMixin, db.Model):
    __tablename__ = "call_log_event"

    id = db.Column(db.Integer, primary_key=True)
    call_sid = db.Column(db.String(255))
    account_sid = db.Column(db.String(255))
    from_number = db.Column(db.String(255))
    to_number = db.Column(db.String(255))
    call_status = db.Column(db.String(255))
    direction = db.Column(db.String(255))
    parent_call_sid = db.Column(db.String(255))
    telco_code = db.Column(db.String(255))
    telco_status = db.Column(db.String(255))
    dial_time = db.Column(db.DateTime)
    pick_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.String(255))
