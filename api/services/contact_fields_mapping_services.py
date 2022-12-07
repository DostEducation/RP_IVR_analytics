from api import models, db, helpers


class ContactFieldsMappingServices(object):
    def __init__(self):
        self.user_phone = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)

    def handle_contact_groups_data(self, jsonData):
        self.set_init_data(jsonData)
        user_groups = jsonData["contact"]["groups"]
        user = models.User.query.get_by_phone(self.user_phone)
        user_id = user.id

        for user_group in user_groups:
            if user_group in user_groups[user_group]:
                self.handle_contact_group_mapping(user_group)

    def handle_contact_group_mapping(self, user_group):
        if not user_group:
            return False

        custom_group_data = models.ContactFieldsMapping.query.get_by_field_name(
            user_group
        )
        if custom_group_data:
            self.process_contact_groups_data(user_group)

    def process_contact_groups_data(self, user_group):
        if user_group:
            class_object = helpers.get_class_by_tablename(user_group.mapped_table_name)
            if class_object:
                column_name = user_group.mapped_table_column_name

            self.update_user_group(class_object, column_name)

    def update_user_group(class_object, user_id, column_name):
        class_object_data = class_object.get_by_user_id(user_id)
        if class_object_data:
            setattr(class_object, user_id, column_name)
            db.session.commit()
