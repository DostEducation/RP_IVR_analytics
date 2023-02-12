from api.mixins import TimestampMixin
from api import db, helpers, models, app
from flask_sqlalchemy import BaseQuery
from api.helpers.common_helper import current_ist_time
from utils.loggingutils import logger


class UserProgramQuery(BaseQuery):
    def create(self, user_id, data):
        try:
            program_id = app.config["DEFAULT_PROGRAM_ID"]
            preferred_time_slot = app.config["DEFAULT_PROGRAM_TIME_CATEGORY"]

            if data.get("program_id"):
                program_id = data["program_id"]

            user_program = UserProgram(
                user_id=user_id,
                program_id=program_id,
                status=data["status"]
                if "status" in data
                else models.UserProgram.UserProgramStatus.IN_PROGRESS,
                start_date=current_ist_time().date(),
                preferred_time_slot=preferred_time_slot,
            )
            helpers.save(user_program)
        except Exception as e:
            logger.error(f"Failed to create user_program for user_id {user_id}: {e}")

    def update(self, user_program_details, data):
        try:
            if data["program_id"]:
                user_program_details.program_id = data["program_id"]

            for key, value in data.items():
                if key == "status":
                    user_program_details.status = value

            db.session.commit()
        except Exception as e:
            logger.error(
                f"Failed to update user program details for user_program_id {user_program_details.id}: {e}"
            )

    def get_latest_active_user_program(self, user_id):
        try:
            return (
                self.filter(
                    UserProgram.user_id == user_id,
                    UserProgram.status
                    == models.UserProgram.UserProgramStatus.IN_PROGRESS,
                )
                .order_by(UserProgram.id.desc())
                .first()
            )
        except Exception as e:
            logger.error(
                f"Failed to fetch the latest active user program for user_id {user_id}. Error message: {e}"
            )

    def get_latest_user_program(self, user_id):
        try:
            return (
                self.filter(
                    UserProgram.user_id == user_id,
                )
                .order_by(UserProgram.id.desc())
                .first()
            )
        except Exception as e:
            logger.error(
                f"Error occurred while fetching latest user program for user_id: {user_id}. Error message: {e}"
            )


class UserProgram(TimestampMixin, db.Model):
    query_class = UserProgramQuery
    __tablename__ = "user_program"

    class UserProgramStatus(object):
        IN_PROGRESS = "in-progress"
        COMPLETE = "complete"
        TERMINATED = "terminated"
        UNSUB = "unsub"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    preferred_time_slot = db.Column(db.String(50))
    status = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    @classmethod
    def get_by_user_id(self, user_id):
        return UserProgram.query.get_latest_active_user_program(user_id)
