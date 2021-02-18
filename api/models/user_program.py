from api.mixins import TimestampMixin
from api import db

class UserProgram(TimestampMixin, db.Model):
    __tablename__ = 'user_program'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    preferred_time_slot = db.Column(db.String(50))
    status = db.Column(db.String(50))
