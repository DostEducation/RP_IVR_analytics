from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class CallLogQuery(BaseQuery):
    def get_by_flow_run_uuid(self, flow_run_uuid):
        return self.filter(CallLog.flow_run_uuid == flow_run_uuid).first()


class CallLog(TimestampMixin, db.Model):
    query_class = CallLogQuery

    class CallCategories:
        SCHEDULED = "scheduled"
        CALLBACK = "callback"
        LIVECALL = "livecall"

    class FlowCategories:
        REGISTRATION = "registration"
        CONTENT = "content"
        NUDGE = "nudge"
        SURVEY = "survey"
        BLAST = "blast"
        OTHER = "other"

    __tablename__ = "call_log"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    registration_id = db.Column(db.Integer, db.ForeignKey("registration.id"))
    program_sequence_id = db.Column(db.Integer, db.ForeignKey("program_sequence.id"))
    content_version_id = db.Column(db.Integer, db.ForeignKey("content_version.id"))
    call_sid = db.Column(db.Integer)
    flow_run_uuid = db.Column(db.String(255))
    call_type = db.Column(db.String(50))
    scheduled_by = db.Column(db.String(100))
    user_phone_number = db.Column(db.String(50), nullable=False)
    system_phone_number = db.Column(db.String(50))
    circle = db.Column(db.String(50))
    status = db.Column(db.String(50))
    listen_seconds = db.Column(db.String(50))
    recording_url = db.Column(db.String(1000))
    dial_time = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    flow_category = db.Column(db.String(50))
    call_category = db.Column(db.String(50))
    parent_flow_run_uuid = db.Column(db.String(255))
    parent_flow_name = db.Column(db.String(255))
    flow_run_created_on = db.Column(db.DateTime)
    content_id = db.Column(db.Integer)
    flow_name = db.Column(db.String(255))
