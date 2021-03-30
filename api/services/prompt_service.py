from api import models, db, helpers


class PromptService(object):
    def __init__(self):
        self.user_phone = None
        self.preferred_time_slot = None
        self.call_log_id = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        flow_run_uuid = helpers.fetch_by_key("run_uuid", jsonData)
        call_log_details = models.CallLog.query.get_by_flow_run_uuid(flow_run_uuid)
        self.call_log_id = call_log_details.id

    def handle_prompt_response(self, jsonData):
        self.set_init_data(jsonData)
        data = jsonData["results"]
        ivr_prompt_response_details = models.IvrPromptResponse.query.get_by_call_log_id(
            self.call_log_id
        )
        user_details = models.User.query.get_by_phone(self.user_phone)
        prompt_program_id = helpers.get_program_prompt_id(jsonData)
        updated_registration_data = {}
        updated_user_data = {}
        for key in data:
            if key != "result" and "category" in data[key] and "name" in data[key]:
                prompt_response = data[key]["category"]
                prompt_name = data[key]["name"]
                ivr_prompt_details = models.IvrPrompt.query.get_by_name(prompt_name)
                if ivr_prompt_details:
                    response_data = self.fetch_prompt_response(data[key]["category"])
                    if "TIME-OPTIN" in prompt_name:
                        self.preferred_time_slot = response_data
                    elif "DISTRICT" in prompt_name:
                        user_district = response_data
                        updated_registration_data["district"] = user_district
                        updated_user_data["district"] = user_district
                    elif "PARENT" in prompt_name:
                        updated_registration_data["parent_type"] = response_data

                response_exists = False
                if ivr_prompt_response_details:
                    response_exists = self.check_if_already_exists(
                        ivr_prompt_response_details, prompt_name, prompt_response
                    )

                if not response_exists:
                    ivr_prompt_data = {}
                    ivr_prompt_data["prompt_name"] = prompt_name
                    ivr_prompt_data["prompt_response"] = prompt_response
                    ivr_prompt_data["keypress"] = data[key]["value"]
                    self.add_prompt_response(ivr_prompt_details, ivr_prompt_data)

        if updated_user_data:
            self.update_user_details(user_details, updated_user_data)
        if user_details and prompt_program_id:
            user_program_data = {}
            if self.preferred_time_slot:
                user_program_data["preferred_time_slot"] = self.preferred_time_slot
            models.UserProgram.query.upsert_user_program(
                user_details.id, prompt_program_id, user_program_data
            )
        if updated_registration_data:
            self.update_registration_details(updated_registration_data)

    def check_if_already_exists(
        self, ivr_prompt_response_details, prompt_name, prompt_response
    ):
        if not ivr_prompt_response_details:
            return False
        for row in ivr_prompt_response_details:
            if row.response == prompt_response and row.prompt_name == prompt_name:
                return True
        return False

    def add_prompt_response(self, ivr_prompt_details, data):
        try:
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
                call_log_id=self.call_log_id,
                keypress=data["keypress"],
            )
            helpers.save(ivr_prompt_response)
        except IndexError:
            print("Exception occured")

    def update_user_details(self, user_details, data):
        if user_details:
            try:
                for key, value in data.items():
                    if key == "district":
                        user_details.district = value
                db.session.commit()
            except IndexError:
                # Need to log this
                print("Failed to update user details")

    def update_registration_details(self, data):
        registrant = models.Registration.query.get_by_phone(self.user_phone)
        if registrant:
            try:
                for key, value in data.items():
                    if key == "district":
                        registrant.district = value
                    if key == "parent_type":
                        registrant.parent_type = value
                db.session.commit()
            except IndexError:
                # Need to log this
                print("Failed to udpate registration details")

    def fetch_prompt_response(self, prompt):
        split_prompt_by_hyphen = helpers.split_prompt_by_hyphen(prompt)
        split_prompt_by_underscore = helpers.split_prompt_by_underscore(
            split_prompt_by_hyphen[-1]
        )
        return (
            split_prompt_by_underscore[1]
            if len(split_prompt_by_underscore) > 1
            else None
        )
