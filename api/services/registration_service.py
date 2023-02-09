# This file is treated as service layer
from api import models, db, helpers, app
from datetime import datetime
from utils.loggingutils import logger


class RegistrationService(object):
    def __init__(self):
        self.system_phone = None
        self.user_phone = None
        self.user_id = None
        self.selected_program_id = app.config["DEFAULT_PROGRAM_ID"]
        self.has_default_program_selection = True
        self.selected_time_slot = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.system_phone = helpers.fetch_by_key("address", jsonData["channel"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        selected_program_id = helpers.get_program_prompt_id(jsonData)
        if selected_program_id:
            self.selected_program_id = selected_program_id
            self.has_default_program_selection = False
            logger.info("User has selected program id: %s", self.selected_program_id)
        else:
            logger.warning(
                "User has not selected program id, using default id: %s",
                self.selected_program_id,
            )

    def handle_registration(self, jsonData):
        try:
            self.set_init_data(jsonData)
            flow_run_uuid = helpers.fetch_by_key(
                "run_uuid", jsonData
            )  # TODO: need to remove this once every flow has flow_run_details variable in webhook
            if "flow_run_details" in jsonData:
                flow_run_uuid = helpers.fetch_by_key(
                    "uuid", jsonData["flow_run_details"]
                )
            if flow_run_uuid:
                call_log = models.CallLog.query.get_by_flow_run_uuid(flow_run_uuid)
                user_program_data = {}
                user_program_data["program_id"] = self.selected_program_id
                if call_log:
                    registration_data = models.Registration.query.get_by_id(
                        call_log.registration_id
                    )
                else:
                    registration_data = models.Registration.query.get_by_phone(
                        self.user_phone
                    )

                if registration_data:
                    self.update_registration(registration_data, jsonData)
                    user_program = (
                        models.UserProgram.query.get_latest_active_user_program(
                            registration_data.user_id
                        )
                    )
                    if user_program:
                        if self.has_default_program_selection:
                            user_program_data["program_id"] = user_program.program_id
                        models.UserProgram.query.update(user_program, user_program_data)
                    else:
                        models.UserProgram.query.create(self.user_id, user_program_data)
                        logger.info(
                            f"Successfully updated user program with ID: {user_program.id}"
                        )
                else:
                    self.register(jsonData)
                    models.UserProgram.query.create(self.user_id, user_program_data)
                    logger.info(
                        f"Successfully created new user program with user ID: {self.user_id}"
                    )
            else:
                logger.warning(f"No flow run UUID found in jsonData: {jsonData}")

        except Exception as e:
            logger.error(f"Failed to handle registration for {self.user_phone}: {e}")

    # Handle new user registration
    def register(self, jsonData):
        system_phone_details = models.SystemPhone.query.get_by_phone(self.system_phone)
        if self.selected_program_id:
            self.user_id = self.create_user(jsonData)

        registration_status = (
            models.Registration.RegistrationStatus.INCOMPLETE
            if self.has_default_program_selection
            else models.Registration.RegistrationStatus.COMPLETE
        )
        if system_phone_details:
            registrant = models.Registration(
                user_phone=self.user_phone,
                system_phone=self.system_phone,
                state=system_phone_details.state,
                status=registration_status,
                program_id=self.selected_program_id,
                partner_id=helpers.get_partner_id_by_system_phone(self.system_phone),
                user_id=self.user_id,
                has_dropped_missedcall=True,
                has_received_callback=True,
                signup_date=datetime.now()
                if registration_status
                == models.Registration.RegistrationStatus.COMPLETE
                else None,
            )
            try:
                helpers.save(registrant)
                logger.info(
                    f"Successfully registered user with phone {self.user_phone}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to save registration data for user with phone {self.user_phone}: {e}"
                )
        else:
            logger.warning(f"System phone not found for {self.system_phone}")

    def update_registration(self, registration, jsonData):
        """Updates the registration data

        Args:
            registration (object): Takes registration as object
            jsonData (json): Takes request json for updating registration fields
        """
        if not registration:
            logger.warning("No registration data found to update.")
            return

        self.user_id = self.create_user(jsonData) if self.selected_program_id else None

        if registration.status != models.Registration.RegistrationStatus.COMPLETE:
            if not (registration.program_id and self.has_default_program_selection):
                # Update the registration program id if the registration is not completed.
                registration.program_id = self.selected_program_id
                logger.info("Updating program_id in the registration.")
            if not self.has_default_program_selection:
                # Update the registration signup date if the registration is not completed.
                registration.signup_date = datetime.now()
                logger.info("Updating signup_date in the registration.")

            registration.status = models.Registration.RegistrationStatus.INCOMPLETE
            if not self.has_default_program_selection:
                registration.status = models.Registration.RegistrationStatus.COMPLETE

        if self.user_id:
            registration.user_id = self.user_id
            registration.has_received_callback = True
            try:
                db.session.commit()
                logger.info("Registration updated successfully.")
            except Exception as e:
                logger.error(
                    f"Failed to update registration for {self.user_phone}: {e}"
                )

    def create_user(self, jsonData):
        user = models.User.query.get_by_phone(self.user_phone)
        system_phone_details = models.SystemPhone.query.get_by_phone(self.system_phone)
        if not user:
            logger.info(
                f"User not found in the database. Creating a new user {self.user_phone}."
            )
            user = models.User(
                state=system_phone_details.state,
                phone=self.user_phone,
                partner_id=helpers.get_partner_id_by_system_phone(self.system_phone),
            )
            helpers.save(user)
        return user.id
