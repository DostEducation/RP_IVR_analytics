from api.mixins import TimestampMixin
from api import db

class CallbackTracker(TimestampMixin, db.Model):
    __tablename__ = 'callback_tracker'
    id = db.Column(db.Integer, primary_key=True)
    missed_call_log_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    preferred_time_slot = db.Column(db.String(50))
    status = db.Column(db.String(50))
