from api import models, db, helpers

class PromptService(object):
    def __init__(self):
        self.user_phone = None
        self.selected_time_slot = None

    def handle_prompt_response(self, jsonData):
        data = jsonData['results']
        user_phone = helpers.fetch_by_key('urn', jsonData['contact'])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        flow_run_uuid = helpers.fetch_by_key('run_uuid', jsonData)
        call_log_details = models.CallLog.query.get_by_flow_run_uuid(flow_run_uuid)
        ivr_prompt_response_details = models.IvrPromptResponse.query.get_by_call_log_id(call_log_details.id)
        print('Here we are with call logs for previous flows')
        print(call_log_details)
        updated_registration_data = {}
        updated_user_data = {}
        for key in data:
            if key != 'result' and 'category' in data[key]:
                prompt_name = helpers.remove_last_string_separated_by(data[key]['category'])
                ivr_prompt_details = models.IvrPrompt.query.get_by_name(prompt_name)
                if ivr_prompt_details:
                    if "TIME-OPTIN" in ivr_prompt_details.prompt_name:
                        self.selected_time_slot = self.fetch_prompt_response(data[key]['category'])

                    if "DISTRICT" in ivr_prompt_details.prompt_name:
                        user_district = self.fetch_prompt_response(data[key]['category'])
                        updated_registration_data['district'] = user_district
                        updated_user_data['district'] = user_district

                    if "PARENT" in ivr_prompt_details.prompt_name:
                        updated_registration_data['parent_type'] = self.fetch_prompt_response(data[key]['category'])

                    response_exists = False
                    if ivr_prompt_response_details:
                        response_exists = self.check_if_already_exists(ivr_prompt_response_details, prompt_name, data[key]['category'])

                    if not response_exists:
                        ivr_prompt_response = models.IvrPromptResponse(
                            prompt_name = ivr_prompt_details.prompt_name,
                            prompt_question = ivr_prompt_details.prompt_question,
                            user_phone = self.user_phone,
                            response = data[key]['category'],
                            content_id = ivr_prompt_details.content_id,
                            call_log_id = call_log_details.id
                        )
                        db.session.add(ivr_prompt_response)
                        db.session.commit()

        if updated_user_data:
            user_details = self.update_user_details(updated_user_data)
            user_program_id = helpers.get_program_prompt_id(jsonData)
            if self.selected_time_slot and user_details:
                models.UserProgram.query.upsert_user_program(user_details.user_id, user_program_id, self.selected_time_slot)

    def check_if_already_exists(self, ivr_prompt_response_details, prompt_name, prompt_response):
        for row in ivr_prompt_response_details:
            if row.response == prompt_response and row.prompt_name == prompt_name:
                return True
        return False

    def update_user_details(self, data):
        user_details = models.User.query.get_by_phone(self.user_phone)
        if user_details:
            try:
                for key, value in data.items():
                    user_details.key = value
                db.session.commit()
                return user_details
            except IndexError:
                # Need to log this
                return "Failed to udpate user details"

    def update_registration_details(user_phone, data):
        registrant = models.Registration.query.get_by_phone(self.user_phone)
        if registrant:
            try:
                for key, value in data.items():
                    registrant.key = value

                db.session.commit()
            except IndexError:
                # Need to log this
                return "Failed to udpate registration details"

    def fetch_prompt_response(self, prompt):
        split_prompt_by_hyphen = helpers.split_prompt_by_hyphen(prompt)
        split_prompt_by_underscore = helpers.split_prompt_by_underscore(split_prompt_by_hyphen[-1])
        return split_prompt_by_underscore[1] if len(split_prompt_by_underscore) > 1 else None
