# This file is treated as service layer
from api import models, db, helpers
from datetime import datetime


class CallLogService(object):
    def __init__(self):
        self.system_phone = None
        self.user_phone = None
        self.flow_run_uuid = None
        self.flow_run_created_on = None
        self.call_log = None
        self.missedcall_flow_identifier = ["missedcall", "missed-call"]
        self.call_category = models.CallLog.CallCategories.SCHEDULED
        self.flow_category = models.CallLog.FlowCategories.OTHER

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.system_phone = helpers.fetch_by_key("address", jsonData["channel"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        self.flow_run_uuid = helpers.fetch_by_key(
            "run_uuid", jsonData
        )  # TODO: need to remove this once every flow has flow_run_details variable in webhook
        self.handle_flow_run_details(jsonData)

    def handle_flow_run_details(self, jsonData):
        """To handle flow run details
        Args:
            jsonData (json): json data that we are getting from webhook
        """
        try:
            if "flow_run_details" in jsonData:
                self.flow_run_uuid = helpers.fetch_by_key(
                    "uuid", jsonData["flow_run_details"]
                )
                self.flow_run_created_on = helpers.fetch_by_key(
                    "created_on", jsonData["flow_run_details"]
                )

        except IndexError:
            print("Failed to fetch flow run details")

    def handle_call_log(self, jsonData):
        try:
            self.set_init_data(jsonData)
            if self.flow_run_uuid:
                self.call_log = models.CallLog.query.get_by_flow_run_uuid(
                    self.flow_run_uuid
                )
                if self.call_log:
                    data = {}
                    user_data = models.User.query.get_by_phone(self.user_phone)
                    data["user_id"] = user_data.id if user_data else None
                    self.update_call_logs(data)
                else:
                    self.create_call_logs(jsonData)
            else:
                print("flow_run_uuid is now available.")
        except IndexError:
            print("Failed to log the call details")

    def create_call_logs(self, jsonData):
        try:
            registration_data = models.Registration.query.get_by_phone(self.user_phone)
            user_data = models.User.query.get_by_phone(self.user_phone)
            parent_flow_data = self.handle_parent_flow(jsonData)
            new_call_log = models.CallLog(
                flow_run_uuid=self.flow_run_uuid,
                flow_run_created_on=self.flow_run_created_on,
                call_type=self.fetch_call_type(),
                scheduled_by=self.fetch_call_scheduled_by(),
                user_phone_number=self.user_phone,
                system_phone_number=helpers.sanitize_phone_string(self.system_phone),
                registration_id=registration_data.id if registration_data else None,
                user_id=user_data.id if user_data else None,
                call_category=self.call_category,
                parent_flow_name=parent_flow_data["parent_flow_name"],
                parent_flow_run_uuid=parent_flow_data["parent_flow_run_uuid"],
                content_id=jsonData["content_id"] if "content_id" in jsonData else None,
                flow_category=jsonData["flow_category"]
                if "flow_category" in jsonData
                else self.flow_category,
            )
            helpers.save(new_call_log)
        except IndexError:
            # Need to log this
            return "Failed to create call log"

    def update_call_logs(self, data):
        try:
            self.call_log.updated_on = datetime.now()
            if "user_id" in data:
                self.call_log.user_id = data["user_id"]
            if "user_module_content_id" in data:
                self.call_log.user_module_content_id = data["user_module_content_id"]
            db.session.commit()
        except IndexError:
            # Need to log this
            return "Failed to udpate call log"

    def fetch_call_type(self):
        return "outbound-call"  # TODO: Need to pass dynamic value

    def fetch_call_scheduled_by(self):
        return "rapidpro"  # TODO: Need to pass dynamic value

    def update_user_module_content_id_in_call_log(self, user_module_content_id):
        if self.call_log and user_module_content_id:
            data = {}
            data["user_module_content_id"] = user_module_content_id
            self.update_call_logs(data)

    def handle_parent_flow(self, jsonData):
        parent_flow_data = {}
        parent_flow_data["parent_flow_name"] = None
        parent_flow_data["parent_flow_run_uuid"] = None
        if "parent" in jsonData and jsonData["parent"] is not None:
            if "flow" in jsonData["parent"]:
                parent_flow = jsonData["parent"]["flow"]
                parent_flow_data["parent_flow_name"] = parent_flow["name"]
                missedcall_category_list = helpers.list_having_string(
                    parent_flow["name"], self.missedcall_flow_identifier
                )
                if missedcall_category_list:
                    """The call category is set to call back if missedcall flow has ran.
                    For that, the missed call flow name should contain string "missedcall"
                    """
                    self.call_category = models.CallLog.CallCategories.CALLBACK
            if "uuid" in jsonData["parent"]:
                parent_flow_data["parent_flow_run_uuid"] = jsonData["parent"]["uuid"]
        return parent_flow_data
