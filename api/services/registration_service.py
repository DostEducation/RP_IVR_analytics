# This file is treated as service layer
from api import models, db, helpers

class RegistrationService:
    def handle_registration(self, jsonData):
        try:
            contact = jsonData['contact']
            user_phone = contact['urn']
            flow_run_uuid = helpers.fetch_by_key('run_uuid', jsonData)
            if flow_run_uuid:
                call_log = models.CallLog.query.get_by_flow_run_uuid(flow_run_uuid)
                if call_log:
                    self.update_registration(call_log.registration_id, jsonData)
                else:
                    self.register(user_phone, jsonData)

            # All the prompt responses are captured with result
            if 'results' in jsonData:
                self.add_prompt_response(user_phone, jsonData['results'])

        except IndexError:
            print("Failed to register")

    # Handle new user registration
    def register(self, user_phone, jsonData):
        system_phone = jsonData['system_phone']
        system_phone_details = models.SystemPhone.query.get_by_phone(system_phone)
        selected_program_id = self.get_program_prompt_id(jsonData)
        user_id = None
        if selected_program_id:
            user_id = self.create_user(user_phone, jsonData)

        registration_status = 'in-progress' if selected_program_id else 'pending'
        if system_phone_details:
            registrant = models.Registration(
                user_phone = helpers.sanitize_phone_string(user_phone),
                system_phone = system_phone,
                state = system_phone_details.state,
                status = 'complete' if user_id else registration_status,
                program_id = selected_program_id,
                user_id = user_id
            )
            db.session.add(registrant)
            db.session.commit()

    def update_registration(self, registration_id, jsonData):
        system_phone = jsonData['system_phone']
        registration = models.Registration.query.get_by_id(registration_id)
        selected_program_id = self.get_program_prompt_id(jsonData)
        user_id = None
        if registration:
            if selected_program_id:
                user_id = self.create_user(registration.user_phone, jsonData)

            registration.program_id = selected_program_id
            if user_id:
                registration.user_id = user_id
                registrant.status = 'complete'
            db.session.commit()

    # Insert Different prompt response
    def add_prompt_response(self, user_phone, data):
        for key in data:
            if key != 'result' and 'category' in data[key]:
                prompt_name = helpers.remove_last_string_separated_by(data[key]['category'])
                irv_prompt_details = models.IvrPrompt.query.get_by_name(prompt_name)
                if irv_prompt_details:
                    ivr_prompt_response = models.IvrPromptResponse(
                        prompt_name = irv_prompt_details.prompt_name,
                        prompt_question = irv_prompt_details.prompt_question,
                        user_phone = user_phone.replace("tel:+", ""),
                        content_id = irv_prompt_details.content_id
                    )
                    db.session.add(ivr_prompt_response)
                    db.session.commit()

    def get_program_prompt_id(self, jsonData):
        if 'program_details' in jsonData:
            program_categories = helpers.fetch_by_key('categories', jsonData['program_details'])
            if 0 in program_categories:
                split_prompt_by_hyphen = helpers.get_split_prompt_by_hyphen(program_categories[0])
                split_prompt_by_underscore = helpers.get_split_prompt_by_underscore(split_prompt_by_hyphen[-1])
                return helpers.fetch_by_key(1, split_prompt_by_underscore)
        return None

    def create_user(user_phone, jsonData):
        user = models.User.query.get_by_phone(user_phone)
        if not user:
            user = models.User(
                system_phone = system_phone,
                state = system_phone_details.state,
                phone = helpers.sanitize_phone_string(user_phone),
                partner_id = helpers.get_partner_id_by_system_phone(system_phone)
            )
            db.session.add(user)
            db.session.commit()
            return user.id
        return None

