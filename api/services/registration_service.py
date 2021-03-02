# This file is treated as service layer
from api import models, db, helpers

class RegistrationService(object):
    def __init__(self):
        self.system_phone = None
        self.user_phone = None

    def handle_registration(self, jsonData):
        try:
            user_phone = helpers.fetch_by_key('urn', jsonData['contact'])
            self.system_phone = helpers.fetch_by_key('address', jsonData['channel'])
            self.user_phone = helpers.sanitize_phone_string(user_phone)
            flow_run_uuid = helpers.fetch_by_key('run_uuid', jsonData)
            if flow_run_uuid:
                call_log = models.CallLog.query.get_by_flow_run_uuid(flow_run_uuid)
                if call_log:
                    self.update_registration(call_log.registration_id, jsonData)
                else:
                    self.register(jsonData)

            # All the prompt responses are captured with results
            if 'results' in jsonData:
                self.add_prompt_response(jsonData['results'])

        except IndexError:
            print("Failed to register")

    # Handle new user registration
    def register(self, jsonData):
        system_phone_details = models.SystemPhone.query.get_by_phone(self.system_phone)
        selected_program_id = self.get_program_prompt_id(jsonData)
        user_id = None
        if selected_program_id:
            user_id = self.create_user(jsonData)

        registration_status = 'in-progress' if selected_program_id else 'pending'
        if system_phone_details:
            registrant = models.Registration(
                user_phone = self.user_phone,
                system_phone = self.system_phone,
                state = system_phone_details.state,
                status = 'complete' if user_id else registration_status,
                program_id = selected_program_id,
                user_id = user_id
            )
            db.session.add(registrant)
            db.session.commit()

    def update_registration(self, registration_id, jsonData):
        registration = models.Registration.query.get_by_id(registration_id)
        selected_program_id = self.get_program_prompt_id(jsonData)
        user_id = None
        if registration:
            if selected_program_id:
                user_id = self.create_user(jsonData)

            registration.program_id = selected_program_id
            if user_id:
                registration.user_id = user_id
                registration.status = 'complete'
            db.session.commit()

    # Insert Different prompt response
    def add_prompt_response(self, data):
        for key in data:
            if key != 'result' and 'category' in data[key]:
                prompt_name = helpers.remove_last_string_separated_by(data[key]['category'])
                irv_prompt_details = models.IvrPrompt.query.get_by_name(prompt_name)
                if irv_prompt_details:
                    ivr_prompt_response = models.IvrPromptResponse(
                        prompt_name = irv_prompt_details.prompt_name,
                        prompt_question = irv_prompt_details.prompt_question,
                        user_phone = self.user_phone,
                        content_id = irv_prompt_details.content_id
                    )
                    db.session.add(ivr_prompt_response)
                    db.session.commit()

    def get_program_prompt_id(self, jsonData):
        if 'program_details' in jsonData:
            program_categories = helpers.fetch_by_key('categories', jsonData['program_details'])
            if len(program_categories) > 0:
                split_prompt_by_hyphen = helpers.get_split_prompt_by_hyphen(program_categories[0])
                split_prompt_by_underscore = helpers.get_split_prompt_by_underscore(split_prompt_by_hyphen[-1])
                return split_prompt_by_underscore[1] if len(split_prompt_by_underscore) > 1 else None
        return None

    def create_user(self, jsonData):
        user = models.User.query.get_by_phone(self.user_phone)
        system_phone_details = models.SystemPhone.query.get_by_phone(self.system_phone)
        if not user:
            user = models.User(
                state = system_phone_details.state,
                phone = self.user_phone,
                partner_id = helpers.get_partner_id_by_system_phone(self.system_phone)
            )
            db.session.add(user)
            db.session.commit()
            return user.id
        return None

