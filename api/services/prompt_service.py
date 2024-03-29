# This file is treated as service layer
from api import db
from datetime import datetime
from api.helpers import prompt_helper, common_helper, db_helper
from utils.loggingutils import logger
from api import models


class PromptService:
    def __init__(self):
        self.user_phone = None
        self.call_log_id = None
        self.content_version_id = None

    def set_init_data(self, jsonData):
        user_phone = common_helper.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = common_helper.sanitize_phone_string(user_phone)
        flow_run_uuid = common_helper.fetch_by_key(
            "run_uuid", jsonData
        )  # Need to remove once we are done with making changes in webhooks
        if "flow_run_details" in jsonData:
            flow_run_uuid = common_helper.fetch_by_key(
                "uuid", jsonData["flow_run_details"]
            )
        call_log_details = models.CallLog.query.get_by_flow_run_uuid(flow_run_uuid)
        self.call_log_id = call_log_details.id
        self.content_version_id = call_log_details.content_version_id

    def handle_prompt_response(self, jsonData):
        try:
            self.set_init_data(jsonData)
            data = jsonData["results"]
            ivr_prompt_response_details = (
                models.IvrPromptResponse.query.get_by_call_log_id(self.call_log_id)
            )

            user_details = models.User.query.get_by_phone(self.user_phone)
            if not user_details:
                logger.error(f"User not found for phone {self.user_phone}.")

            for key in data:
                if key != "result" and "category" in data[key] and "name" in data[key]:
                    prompt_response = data[key]["category"]
                    prompt_name = data[key]["name"]
                    ivr_prompt_details = (
                        models.IvrPrompt.query.get_by_name_and_response(
                            prompt_name, prompt_response
                        )
                    )
                    if not ivr_prompt_details and prompt_response.lower() != "other":
                        logger.error(
                            f"IVR prompt not found for name '{prompt_name}' and response '{prompt_response}'"
                        )

                    if ivr_prompt_details:
                        prompt_response_value = self.fetch_prompt_response(
                            data[key]["category"]
                        )
                        self.handle_prompt_mapping(
                            user_details,
                            ivr_prompt_details,
                            prompt_response_value,
                        )

                    response_exists = False
                    if ivr_prompt_response_details:
                        response_exists = self.if_exists(
                            ivr_prompt_response_details, prompt_name, prompt_response
                        )

                    if not response_exists:
                        ivr_prompt_data = {}
                        ivr_prompt_data["prompt_name"] = prompt_name
                        ivr_prompt_data["prompt_response"] = prompt_response
                        ivr_prompt_data["keypress"] = data[key]["value"]
                        if jsonData.get("log_created_on", None):
                            ivr_prompt_data["log_created_on"] = jsonData[
                                "log_created_on"
                            ]
                        self.add_prompt_response(ivr_prompt_details, ivr_prompt_data)
        except Exception as e:
            logger.error(
                f"Failed to handle prompt response for user phone {self.user_phone}. Error: {e}"
            )

    def if_exists(self, ivr_prompt_response_details, prompt_name, prompt_response):
        if not ivr_prompt_response_details:
            return False
        for row in ivr_prompt_response_details:
            if row.response == prompt_response and row.prompt_name == prompt_name:
                return True
        return False

    def add_prompt_response(self, ivr_prompt_details, data):
        try:
            keypress = self.sanitize_keypress(data)
            ivr_prompt_response = models.IvrPromptResponse(
                prompt_name=data["prompt_name"],
                prompt_question=ivr_prompt_details.prompt_question
                if ivr_prompt_details
                else None,
                user_phone=self.user_phone,
                response=data["prompt_response"],
                content_id=ivr_prompt_details.content_id
                if ivr_prompt_details
                else None,
                content_version_id=self.content_version_id,
                call_log_id=self.call_log_id,
                keypress=keypress,
                created_on=data["log_created_on"]
                if data.get("log_created_on", None)
                else datetime.utcnow(),
            )
            db_helper.save(ivr_prompt_response)
        except Exception as e:
            logger.error(
                f"An error occurred while adding prompt response for {self.user_phone}. Error: {e}"
            )

    def fetch_prompt_response(self, prompt):
        split_prompt_by_underscore = prompt_helper.split_the_prompt_by_underscore(
            prompt
        )

        return split_prompt_by_underscore[-1]

    def handle_prompt_mapping(
        self, user_details, ivr_prompt_details, prompt_response_value
    ):
        """This function will be populating different other table column based on the user prompt response.
        Note: The table need to be associated with user.
        """
        try:
            if not user_details:
                return False

            ivr_prompt_mapping_data = (
                models.IvrPromptMapping.query.get_by_ivr_prompt_id(
                    ivr_prompt_details.id
                )
            )
            if ivr_prompt_mapping_data:
                # It means mapping exists
                self.process_mapped_fields(
                    user_details, ivr_prompt_mapping_data, prompt_response_value
                )
            return True
        except Exception as e:
            logger.error(
                f"Exception occurred while handling prompt mapping for user phone {self.user_phone}. Error message: {e}"
            )
            return None

    def process_mapped_fields(
        self, user_details, ivr_prompt_mapping_data, prompt_response_value
    ):
        try:
            for mapped_class in ivr_prompt_mapping_data:
                class_object = db_helper.get_class_by_tablename(
                    mapped_class.mapped_table_name
                )
                if class_object:
                    column_name = mapped_class.mapped_table_column_name

                    column_data_type = prompt_helper.get_column_data_type(
                        mapped_class.mapped_table_name, column_name
                    )

                    if column_data_type == "boolean":
                        if prompt_response_value.upper() == "YES":
                            prompt_response_value = True
                        elif prompt_response_value.upper() == "NO":
                            prompt_response_value = False
                        else:
                            prompt_response_value = None

                    elif (
                        not prompt_response_value
                        or prompt_response_value.lower() == "other"
                    ):
                        prompt_response_value = mapped_class.default_value

                    self.update_mapped_fields(
                        class_object,
                        user_details,
                        column_name,
                        prompt_response_value,
                    )
        except Exception as e:
            logger.error(
                f"Failed to process mapped fields for prompt value '{prompt_response_value}' and for "
                f"user phone {self.user_phone}. Error message:{e}"
            )

    def update_mapped_fields(
        self, class_object, user_details, column_name, prompt_response_value
    ):
        try:
            class_object_data = class_object.get_by_user_id(user_details.id)
            if class_object_data:
                setattr(class_object_data, column_name, prompt_response_value)
                db.session.commit()
        except Exception as e:
            logger.error(
                f"Exception occurred while updating mapped fields for prompt response value {prompt_response_value} "
                f"and for user phone {self.user_phone}. Error message {e}"
            )

    def sanitize_keypress(self, data):
        keypress = data["keypress"]
        try:
            if keypress and str(keypress).isdigit() and len(keypress) < 5:
                return_keypress_value = int(keypress)
            else:
                return_keypress_value = -2
        except Exception as e:
            logger.error(
                f"Keypress value by {self.user_phone} is not an integer. Error message: {e}"
            )
            return_keypress_value = -2

        return return_keypress_value
