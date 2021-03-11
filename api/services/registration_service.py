# This file is treated as service layer
from api import models, db, helpers

class RegistrationService(object):
    def __init__(self):
        self.system_phone = None
        self.user_phone = None
        self.user_id = None
        self.selected_program_id = None
        self.selected_time_slot = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key('urn', jsonData['contact'])
        self.system_phone = helpers.fetch_by_key('address', jsonData['channel'])
        self.user_phone = helpers.sanitize_phone_string(user_phone)

    def handle_registration(self, jsonData):
        try:
            self.set_init_data(jsonData)
            self.register(jsonData)
        except IndexError:
            print("Failed to register")

    def update_registration_details(self, jsonData):
        try:
            self.set_init_data(jsonData)
            registration_details = models.Registration.query.get_latest_by_phone(self.user_phone)
            if registration_details:
                self.update(registration_details.id, jsonData)
        except IndexError:
            print("Failed to update registeration data")

    # Handle new user registration
    def register(self, jsonData):
        system_phone_details = models.SystemPhone.query.get_by_phone(self.system_phone)
        self.selected_program_id = helpers.get_program_prompt_id(jsonData)
        if self.selected_program_id:
            self.user_id = self.create_user(jsonData)

        registration_status = 'in-progress' if self.selected_program_id else 'pending'
        if system_phone_details:
            registrant = models.Registration(
                user_phone = self.user_phone,
                system_phone = self.system_phone,
                state = system_phone_details.state,
                status = 'complete' if self.user_id else registration_status,
                program_id = self.selected_program_id,
                user_id = self.user_id,
                has_dropped_missedcall = True
            )
            helpers.save(registrant)

    def update(self, registration_id, jsonData):
        registration = models.Registration.query.get_by_id(registration_id)
        self.selected_program_id = helpers.get_program_prompt_id(jsonData)
        if registration:
            self.user_id = self.create_user(jsonData) if self.selected_program_id else None
            registration.program_id = self.selected_program_id
            if self.user_id:
                registration.user_id = self.user_id
                registration.status = 'complete'
                registration.has_received_callback = True
                registration.partner_id = helpers.get_partner_id_by_system_phone(self.system_phone)
            db.session.commit()

    def create_user(self, jsonData):
        user = models.User.query.get_by_phone(self.user_phone)
        system_phone_details = models.SystemPhone.query.get_by_phone(self.system_phone)
        if not user:
            user = models.User(
                state = system_phone_details.state,
                phone = self.user_phone,
                partner_id = helpers.get_partner_id_by_system_phone(self.system_phone)
            )
            helpers.save(user)
            return user.id
        return None
