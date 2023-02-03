# This file is treated as service layer
from api import models, helpers, db
from api.helpers.common_helper import current_ist_time
import logging

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UserProgramService(object):
    def __init__(self):
        self.user_id = None
        self.user_phone = None
        self.user_program_data = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        user = models.User.query.get_by_phone(self.user_phone)
        self.user_id = user.id
