# This file is treated as service layer
from api import models, db, helpers, app
from datetime import datetime
from utils.loggingutils import logger


class CallLogService:
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
            elif "run_uuid" in jsonData:
                self.flow_run_uuid = helpers.fetch_by_key(
                    "run_uuid", jsonData
                )  # Keeping this code to establish backward campatibility:

        except Exception as e:
            logger.error(
                f"Failed to fetch flow run details for user phone {self.user_phone}. Error message: {e}"
            )

    def get_custom_fields_from_webhook_payload(self, data):
        custom_fields = {}
        if data.get("contact") and data["contact"].get("fields"):
            custom_fields = data["contact"].get("fields")
        return custom_fields

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
                    custom_fields = self.get_custom_fields_from_webhook_payload(
                        jsonData
                    )
                    if "content_id" in jsonData:
                        data["content_id"] = jsonData.get("content_id")
                    if "language_id" in custom_fields:
                        data["language_id"] = (
                            custom_fields.get("language_id")
                            if custom_fields.get("language_id")
                            else app.config["DEFAULT_LANGUAGE_ID"]
                        )

                    data["user_id"] = user_data.id if user_data else None
                    self.update_call_logs(data)
                else:
                    self.create_call_logs(jsonData)
        except Exception as e:
            logger.error(
                f"Failed to handle call log details for {self.user_phone}. Error: {e}"
            )

    def create_call_logs(self, jsonData):
        try:
            registration_data = models.Registration.query.get_by_phone(self.user_phone)
            user_data = models.User.query.get_by_phone(self.user_phone)
            parent_flow_data = self.handle_parent_flow(jsonData)
            flow_name = None
            if "flow" in jsonData and jsonData["flow"] is not None:
                flow_name = helpers.fetch_by_key("name", jsonData["flow"])

            content_id = None
            content_version_id = None

            if "content_id" in jsonData:
                content_id = jsonData["content_id"]
                content_data = models.Content.query.get_by_id(content_id)
                custom_fields = self.get_custom_fields_from_webhook_payload(jsonData)
                language_id = (
                    custom_fields.get("language_id")
                    if custom_fields.get("language_id")
                    else app.config["DEFAULT_LANGUAGE_ID"]
                )
                content_version_id = self.get_content_version_id(
                    content_id, language_id
                )

                if not content_data:
                    # If the content id is not available in the system, it will throw the error.
                    # Mark it as None
                    content_id = None
                    content_version_id = None

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
                content_id=content_id,
                content_version_id=content_version_id,
                flow_name=flow_name,
                flow_category=jsonData["flow_category"]
                if "flow_category" in jsonData
                else self.flow_category,
                created_on=jsonData["log_created_on"]
                if jsonData.get("log_created_on", None)
                else datetime.utcnow(),
            )
            helpers.save(new_call_log)
            self.call_log = new_call_log
        except Exception as e:
            logger.error(
                f"Failed to create call log for {self.user_phone}. Error message: {e}"
            )

    def update_call_logs(self, data):
        try:
            self.call_log.updated_on = datetime.utcnow()
            if "user_id" in data:
                self.call_log.user_id = data["user_id"]
            if "program_sequence_id" in data:
                self.call_log.program_sequence_id = data["program_sequence_id"]
            if "content_id" in data and "language_id" in data:
                content_version_id = self.get_content_version_id(
                    data["content_id"], data["language_id"]
                )
                if content_version_id:
                    self.call_log.content_version_id = content_version_id

            db.session.commit()
        except Exception as e:
            logger.error(
                f"Failed to update call log for {self.user_phone}. Error message: {e}"
            )

    def get_content_version_id(self, content_id, language_id):
        content_version = models.ContentVersion.query.get_by_language_and_content_id(
            language_id, content_id
        )

        if not content_version:
            content_version = (
                models.ContentVersion.query.get_by_language_and_content_id(
                    app.config["DEFAULT_LANGUAGE_ID"], content_id
                )
            )

        return content_version.id if content_version else None

    def fetch_call_type(self):
        return "outbound-call"  # TODO: Need to pass dynamic value

    def fetch_call_scheduled_by(self):
        return "rapidpro"  # TODO: Need to pass dynamic value

    def update_program_sequence_id_in_call_log(self, program_sequence_id):
        if self.call_log and program_sequence_id:
            data = {}
            data["program_sequence_id"] = program_sequence_id
            try:
                self.update_call_logs(data)
            except Exception as e:
                logger.error(
                    f"Failed to update program sequence id in call log for {self.user_phone}. Error message: {e}"
                )

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
                    # The call category is set to call back if missedcall flow has ran.
                    # For that, the missed call flow name should contain string "missedcall"
                    self.call_category = models.CallLog.CallCategories.CALLBACK
            if "uuid" in jsonData["parent"]:
                parent_flow_data["parent_flow_run_uuid"] = jsonData["parent"]["uuid"]
        return parent_flow_data
