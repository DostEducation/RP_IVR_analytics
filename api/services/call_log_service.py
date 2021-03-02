# This file is treated as service layer
from api import models, db, helpers
from datetime import datetime

class CallLogService:

    def handle_call_log(self, jsonData):
        try:
            contact = jsonData['contact']
            user_phone = contact['urn']
            flow_run_uuid = self.fetch_flow_run_uuid(jsonData)
            if flow_run_uuid:
                # self.create_call_logs(user_phone, jsonData)
                call_log = models.CallLog.query.get_by_flow_run_uuid(flow_run_uuid)
                if call_log:
                    self.update_call_logs(call_log, jsonData)
                else:
                    self.create_call_logs(user_phone, jsonData)
        except IndexError:
            print("Failed to log the call details")

    def update_call_logs(self, call_log, jsonData):
        try:
            # Check if we need to update call logs
            call_log.flow_run_uuid = self.fetch_flow_run_uuid(jsonData)
            call_log.updated_on = datetime.now()
            db.session.commit()
        except Exception as e:
             # Need to log this
            return "Failed to udpate call log"

    def create_call_logs(self, user_phone, jsonData):
        try:
            registration_data = models.Registration.query.get_by_phone(user_phone)
            new_call_log = models.CallLog(
                flow_run_uuid = self.fetch_flow_run_uuid(jsonData),
                call_type =  self.fetch_call_type(jsonData),
                scheduled_by =  self.fetch_call_scheduled_by(jsonData),
                user_phone_number =  helpers.sanitize_phone_string(user_phone),
                system_phone_number = helpers.sanitize_phone_string(jsonData['system_phone']),
                registration_id = registration_data.id if registration_data else None,
            )
            db.session.add(new_call_log)
            db.session.commit()
        except IndexError:
            # Need to log this
            return "Failed to create call log"

    def fetch_flow_run_uuid(self, jsonData):
        if 'run_uuid' in jsonData:
            return jsonData['run_uuid']
        return None

    def fetch_call_type(self, jsonData):
        return 'outbound-call' # TODO: Need to pass dynamic value

    def fetch_call_scheduled_by(self, jsonData):
        return 'rapidpro' # TODO: Need to pass dynamic value
