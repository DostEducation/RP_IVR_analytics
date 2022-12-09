from api import models, db, helpers


class ContactFieldsMappingService(object):
    def __init__(self):
        self.user_phone = None
        self.user_id = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        user = models.User.query.get_by_phone(self.user_phone)
        self.user_id = user.id

    def handle_custom_fields_data(self, jsonData):
        self.set_init_data(jsonData)
        user_groups = jsonData["contact"]["groups"]
        custom_fields = jsonData["contact"]["fields"]
        user_program = models.UserProgram.query.get_latest_active_user_program(
            self.user_id
        )

        if user_program:
            for user_group in user_groups:
                if user_group in user_groups[user_group]:
                    self.handle_contact_group_mapping(user_group)

            if custom_fields:
                self.handle_contact_filed_mapping(custom_fields)

    def handle_contact_group_mapping(self, user_group):
        if not user_group:
            return False

        custom_group_data = models.ContactFieldsMapping.query.get_by_field_name(
            user_group
        )
        for custom_group in custom_group_data:
            self.process_contact_groups_and_fields_data(custom_group)

    def handle_contact_filed_mapping(self, custom_fields):
        if not custom_fields:
            return False

        custom_fields_data = models.ContactFieldsMapping.query.get_by_field_name(
            custom_fields
        )
        for custom_field in custom_fields_data:
            if custom_field:
                self.process_contact_groups_and_fields_data(custom_field)

    def process_contact_groups_and_fields_data(self, custom_group, custom_field):
        if custom_group:
            class_object = helpers.get_class_by_tablename(
                custom_group.mapped_table_name
            )
            if class_object:
                column_name = custom_group.mapped_table_column_name

            self.update_user_group(class_object, column_name)
        elif custom_field:
            class_object = helpers.get_class_by_tablename(
                custom_field.mapped_table_name
            )
            if class_object:
                column_name = custom_field.mapped_table_column_name

            self.update_user_group(class_object, column_name)

    def update_user_group(self, class_object, column_name):
        class_object_data = class_object.get_by_user_id(self.user_id)
        if class_object_data:
            setattr(class_object, column_name)
            db.session.commit()
