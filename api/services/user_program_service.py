# This file is treated as service layer
from api import models, helpers, db
from api.helpers.common_helper import current_ist_time


class UserProgramService:
    def __init__(self):
        self.user_id = None
        self.user_phone = None
        self.user_program_data = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        user = models.User.query.get_by_phone(self.user_phone)
        self.user_id = user.id

    def update_user_program_status(self, JsonData, status):
        self.set_init_data(JsonData)
        self.user_program_data = models.UserProgram.get_by_user_id(self.user_id)
        if self.user_program_data:
            self.user_program_data.status = status
            self.user_program_data.end_date = current_ist_time().date()
            db.session.commit()
