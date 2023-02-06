from api import models, helpers


class ProgramSequenceService(object):
    def __init__(self):
        self.content_id = None
        self.user_phone = None

    def set_init_data(self, jsonData):
        self.content_id = jsonData["content_id"]
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)

    def get_program_sequence_id(self, jsonData):
        self.set_init_data(jsonData)
        try:
            user_details = models.User.query.get_by_phone(self.user_phone)
            if not user_details:
                # Need to log this
                print("User not available")
                return None

            module_content_details = models.ModuleContent.query.get_by_content_id(
                self.content_id
            )

            if not module_content_details:
                # it is optional to have Content and Module association
                return None

            program_module_details = models.ProgramModule.query.get_by_module_id(
                module_content_details.module_id
            )

            user_program_details = (
                models.UserProgram.query.get_latest_active_user_program(user_details.id)
            )

            if not user_program_details:
                user_program_details = models.UserProgram.query.get_latest_user_program(
                    user_details.id
                )

            if not user_program_details:
                # Need to log this
                return None

            program_sequence = (
                models.ProgramSequence.query.get_by_module_content_program_ids(
                    program_module_details.program_id,
                    program_module_details.module_id,
                    self.content_id,
                )
            )
            program_sequence_id = None

            if program_sequence:
                program_sequence_id = program_sequence.id

            return program_sequence_id
        except Exception as e:
            print(f"Exception occured:{e}")
