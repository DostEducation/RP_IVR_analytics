from api.mixins import TimestampMixin
from api import db, helpers
from flask_sqlalchemy import BaseQuery

class UserProgramQuery(BaseQuery):

    def upsert_user_program(self, user_id, program_id, data):
        user_program_details = self.get_by_user_and_program_ids(user_id, program_id)
        preferred_time_slot = data['preferred_time_slot'] if 'preferred_time_slot' in data else None
        if user_program_details:
            program_data = {}
            program_data['preferred_time_slot'] = preferred_time_slot
            program_data['status'] = data['status'] if 'status' in data else None
            self.update(user_program_details, data)
        else:
            user_program = UserProgram(
                user_id = user_id,
                program_id = program_id,
                preferred_time_slot = preferred_time_slot,
                status = data['status'] if 'status' in data else 'in-progress'
            )
            helpers.save(user_program)

    def update(self, user_program_details, data):
        try:
            for key, value in data.items():
                if key == 'preferred_time_slot':
                    user_program_details.preferred_time_slot = value
                elif key == 'status':
                    user_program_details.status = value
            db.session.commit()
        except IndexError:
            return "Failed to udpate user program details"

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
