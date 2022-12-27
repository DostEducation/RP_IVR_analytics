from api import models, db, helpers


class ContactFieldsMappingService(object):
    def __init__(self):
        self.user_phone = None
        self.user_id = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)

    def handle_contact_fields_data(self, jsonData):
        self.set_init_data(jsonData)
        user_groups = jsonData["contact"]["groups"]
        contact_fields = jsonData["contact"]["fields"]
        user_details = models.User.query.get_by_phone(self.user_phone)
        user_program = models.UserProgram.query.get_latest_active_user_program(
            user_details.id
        )

        if user_program:
            if user_groups:
                for user_group in user_groups:
                    user_group_name = user_group["name"]
                    user_group_details = (
                        models.ContactFieldsMapping.query.get_by_group_and_field_name(
                            user_group_name
                        )
                    )
                    print(user_group_details)
                    if user_group_details:
                        self.process_contact_groups_data(
                            user_group_details, user_details
                        )

            if contact_fields:
                user_contact_field_details = (
                    models.ContactFieldsMapping.query.get_by_group_and_field_name(
                        contact_fields
                    )
                )
                if user_contact_field_details:
                    self.process_contact_fields_data(
                        user_contact_field_details, user_details
                    )

    # def handle_contact_group_mapping(self, user_group_details, user_group):
    #     if not user_group:
    #         return False

    #     contact_group_data = models.ContactFieldsMapping.query.get_by_group_and_field_id(
    #         user_group_details.id
    #     )
    #     if contact_group_data:
    #         self.process_contact_groups_data(contact_group_data)

    # def handle_contact_filed_mapping(self, user_contact_field_details, contact_fields):
    #     print("hello")
    #     if not contact_fields:
    #         return False

    #     contact_fields_data = models.ContactFieldsMapping.query.get_by_group_and_field_id(
    #         user_contact_field_details.id
    #     )
    #     if contact_fields_data:
    #         self.process_contact_fields_data(contact_fields_data)

    def process_contact_groups_data(self, user_group_details, user_details):
        try:
            if user_group_details:
                for user_group_detail in user_group_details:
                    class_object = helpers.get_class_by_tablename(
                        user_group_detail.mapped_table_name
                    )
                    if class_object:
                        column_name = user_group_detail.mapped_table_column_name

                    self.update_mapped_fields(class_object, column_name, user_details)
        except Exception as e:
            print(e)

    def process_contact_fields_data(self, user_contact_field_details, user_details):
        try:
            if user_contact_field_details:
                for user_contact_field_detail in user_contact_field_details:
                    class_object = helpers.get_class_by_tablename(
                        user_contact_field_detail.mapped_table_name
                    )
                    if class_object:
                        column_name = user_contact_field_detail.mapped_table_column_name

                    self.update_mapped_fields(class_object, column_name, user_details)
        except Exception as e:
            print(e)

    def update_mapped_fields(self, class_object, column_name, user_details):
        class_object_data = class_object.get_by_user_id(user_details.id)
        if class_object_data:
            setattr(class_object, column_name)
            db.session.commit()
