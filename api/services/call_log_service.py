# This file is treated as service layer
from api import models, db, helpers

class CallLogService:
    def handle_call_log(self, jsonData):
        try:
            contact = jsonData['contact']
            user_phone = contact['urn']
            self.create_call_logs(user_phone, jsonData)
        except IndexError:
            print("Failed to log the call details")

    # Handle new user registration
    def create_call_logs(self, user_phone, jsonData):
        call_log = models.CallLog(
            flow_run_uuid = self.fetch_flow_run_uuid(jsonData),
            call_type =  self.fetch_call_type(jsonData),
            scheduled_by =  self.fetch_call_scheduled_by(jsonData),
            user_phone_number =  helpers.sanitize_phone_string(user_phone),
            system_phone_number = helpers.sanitize_phone_string(jsonData['system_phone']),
            # registration_id =  jsonData[''],
            # user_id =  data[''],
        )
        db.session.add(call_log)
        db.session.commit()

    def fetch_flow_run_uuid(self, jsonData):
        if 'run_uuid' in jsonData:
            return jsonData['run_uuid']
        return None

    def fetch_call_type(self, jsonData):
        return 'outbound-call' # TODO: Need to pass dynamic value

    def fetch_call_scheduled_by(self, jsonData):
        return 'rapidpro' # TODO: Need to pass dynamic value
