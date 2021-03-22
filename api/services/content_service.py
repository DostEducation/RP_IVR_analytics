from api import models, db, helpers


class ContentService(object):
    def __init__(self):
        self.content_id = None
        self.user_phone = None

    def set_init_data(self, jsonData):
        self.content_id = jsonData["content_id"]
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)

    def add_user_module_content(self, jsonData):
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
            program_module_details = models.ProgramModule.query.get_by_module_id(
                module_content_details.module_id
            )
            user_program_details = (
                models.UserProgram.query.get_latest_active_user_program(user_details.id)
            )
            if not user_program_details:
                # Need to log this
                print("User program details are not available")
                return None
            user_module_content_data = (
                models.UserModuleContent.query.get_user_module_content(
                    user_program_details.id,
                    program_module_details.id,
                    module_content_details.id,
                )
            )
            if not user_module_content_data:
                user_module_content = models.UserModuleContent(
                    module_content_id=module_content_details.id,
                    program_module_id=program_module_details.id,
                    user_program_id=user_program_details.id,
                    status="complete",
                )
                helpers.save(user_module_content)
                return user_module_content.id
        except IndexError:
            # Need to log this
            print("Failed to add user module content")
            return None
