from api.mixins import TimestampMixin
from api import db

class UserProgramQuery(BaseQuery):

	def upsert_user_program(self, user_id, program_id, preferred_time_slot = 'morning'):
		user_program = UserProgram(
			user_id = user_id, 
			program_id = program_id,
			preferred_time_slot = preferred_time_slot,
		)
		db.session.add(user_program)
		return db.session.commit()

class UserProgram(TimestampMixin, db.Model):
	query_class = UserProgramQuery
    __tablename__ = 'user_program'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    preferred_time_slot = db.Column(db.String(50))
    status = db.Column(db.String(50))
