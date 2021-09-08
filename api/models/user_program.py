from api.mixins import TimestampMixin
from api import db, helpers, models, app
from flask_sqlalchemy import BaseQuery


class UserProgramQuery(BaseQuery):
    def upsert_user_program(self, user_id, data):
        user_program_details = self.get_latest_active_user_program(user_id)
        if not user_program_details:
            self.create(user_id, data)
        else:
            self.update(user_program_details, data)

    def create(self, user_id, data):
        program_id = app.config["DEFAULT_PROGRAM_ID"]
        preferred_time_slot = "AFTERNOON"

        if data["program_id"]:
            program_id = data["program_id"]

        if data["preferred_time_slot"]:
            preferred_time_slot = data["preferred_time_slot"]

        user_program = UserProgram(
            user_id=user_id,
            program_id=program_id,
            status=data["status"]
            if "status" in data
            else models.UserProgram.UserProgramStatus.IN_PROGRESS,
            preferred_time_slot=preferred_time_slot,
        )
        helpers.save(user_program)

    def update(self, user_program_details, data):
        try:
            if data["program_id"]:
                user_program_details.program_id = data["program_id"]

            for key, value in data.items():
                if key == "status":
                    user_program_details.status = value

            db.session.commit()
        except:
            return "Failed to update user program details"

    def get_latest_active_user_program(self, user_id):
        return (
            self.filter(
                UserProgram.user_id == user_id,
                UserProgram.status == models.UserProgram.UserProgramStatus.IN_PROGRESS,
            )
            .order_by(UserProgram.id.desc())
            .first()
        )


class UserProgram(TimestampMixin, db.Model):
    query_class = UserProgramQuery
    __tablename__ = "user_program"

    class UserProgramStatus(object):
        IN_PROGRESS = "in-progress"
        COMPLETE = "complete"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    preferred_time_slot = db.Column(db.String(50))
    status = db.Column(db.String(50))

    @classmethod
    def get_by_user_id(self, user_id):
        return UserProgram.query.get_latest_active_user_program(user_id)
