# This file is treated as service layer
from api import models, db, helpers
from datetime import datetime

class CallLogService(object):
    def __init__(self):
        self.system_phone = None
        self.user_phone = None
        self.flow_run_uuid = None

    def handle_call_log(self, jsonData):
        try:
            user_phone = helpers.fetch_by_key('urn', jsonData['contact'])
            self.system_phone = helpers.fetch_by_key('address', jsonData['channel'])
            self.user_phone = helpers.sanitize_phone_string(user_phone)
            self.flow_run_uuid = helpers.fetch_by_key('run_uuid', jsonData)
            if self.flow_run_uuid:
                call_log = models.CallLog.query.get_by_flow_run_uuid(self.flow_run_uuid)
                if call_log:
                    self.update_call_logs(call_log, jsonData)
                else:
                    self.create_call_logs(jsonData)
        except IndexError:
            print("Failed to log the call details")

    def create_call_logs(self, jsonData):
        try:
            registration_data = models.Registration.query.get_by_phone(self.user_phone)
            user_data = models.User.query.get_by_phone(self.user_phone)
            new_call_log = models.CallLog(
                flow_run_uuid = self.flow_run_uuid,
                call_type =  self.fetch_call_type(),
                scheduled_by =  self.fetch_call_scheduled_by(),
                user_phone_number =  self.user_phone,
                system_phone_number = helpers.sanitize_phone_string(self.system_phone),
                registration_id = registration_data.id if registration_data else None,
                user_id = user_data.id if user_data else None,
            )
            helpers.save(new_call_log)
        except IndexError:
            # Need to log this
            return "Failed to create call log"

    def update_call_logs(self, call_log, jsonData):
        try:
            call_log.flow_run_uuid = self.flow_run_uuid
            call_log.updated_on = datetime.now()
            db.session.commit()
        except IndexError:
             # Need to log this
            return "Failed to udpate call log"

    def fetch_call_type(self):
        return 'outbound-call' # TODO: Need to pass dynamic value

    def fetch_call_scheduled_by(self):
        return 'rapidpro' # TODO: Need to pass dynamic value
