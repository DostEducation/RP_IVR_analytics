from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery

class UserProgramQuery(BaseQuery):

    def upsert_user_program(self, user_id, program_id, preferred_time_slot = None):
        user_program_data = self.get_by_user_and_program_ids(user_id, program_id)
        if not user_program_data:
            user_program = UserProgram(
                user_id = user_id, 
                program_id = program_id,
                preferred_time_slot = preferred_time_slot,
                status = 'active'
            )
            db.session.add(user_program)
            db.session.commit()

    def get_by_user_and_program_ids(self, user_id, program_id):
        return self.filter(UserProgram.user_id == user_id, UserProgram.program_id == program_id).first()

class UserProgram(TimestampMixin, db.Model):
    query_class = UserProgramQuery
    __tablename__ = 'user_program'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    preferred_time_slot = db.Column(db.String(50))
    status = db.Column(db.String(50))
