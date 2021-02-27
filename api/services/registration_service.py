# This file is treated as service layer
from api import models, db, helpers

class RegistrationService:
    def handle_registration(self, jsonData):
        try:
            contact = jsonData['contact']
            user_phone = contact['urn']
            self.register(user_phone, jsonData)
            if 'results' in jsonData:
                self.add_prompt_response(user_phone, jsonData['results'])

        except IndexError:
            print("Failed to register")


    # Handle new user registration
    def register(self, user_phone, jsonData):
        system_phone = jsonData['system_phone']
        system_phone_details = models.SystemPhone.query.get_by_phone(system_phone)
        split_prompt_by_hyphen = helpers.get_split_prompt_by_hyphen(jsonData)
        split_prompt_by_underscore = helpers.get_split_prompt_by_underscore(split_prompt_by_hyphen[-1])
        if system_phone_details:
            registrant = models.Registration(
                user_phone = helpers.sanitize_phone_string(user_phone),
                system_phone = system_phone,
                state = system_phone_details.state,
                status ='Pending',
                program_id = split_prompt_by_underscore[1]
            )
            db.session.add(registrant)
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
