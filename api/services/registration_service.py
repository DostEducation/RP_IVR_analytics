# This file is treated as service layer
from api import models, db, helpers

class RegistrationService:
    ### Main function, used to getting called from cloud function
    def handle_registration(self, jsonData):
        try:
            contact = jsonData['contact']
            user_phone = contact['urn']
            # self.register(user_phone, jsonData)
            if len(jsonData['results']):
                self.add_prompt_response(user_phone, jsonData['results'])
            # self.add_prompt_response(user_phone, jsonData)

        except IndexError:
            print("Failed to register")

    def register(self, user_phone, jsonData):
        system_phone = jsonData['system_phone']
        system_phone_details = models.SystemPhone.query.get_by_phone(system_phone)
        split_prompt_by_hyphen = helpers.get_split_prompt_by_hyphen(jsonData)
        split_prompt_by_underscore = helpers.get_split_prompt_by_underscore(split_prompt_by_hyphen[-1])
        print(split_prompt_by_hyphen, split_prompt_by_underscore)
        if system_phone_details:
            registrant_state = system_phone_details.state
            registrant = models.Registration(
                user_phone = user_phone.replace("tel:+", ""),
                system_phone = system_phone,
                state = registrant_state,
                status ='Pending',
                program_id = split_prompt_by_underscore[1]
            )
            db.session.add(registrant)
            db.session.commit()

    def add_prompt_response(self, user_phone, data):
        for key in data:
            if key != 'result' and len(data[key]['category']):
                prompt_name = helpers.remove_last_string_separated_by(data[key]['category'])
                print(prompt_name)
