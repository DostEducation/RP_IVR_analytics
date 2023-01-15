from api import models, db, helpers


class ContactFieldsMappingService(object):
    def __init__(self):
        self.user_phone = None

    def set_init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)

    def handle_contact_fields_data(self, jsonData):
        try:
            self.set_init_data(jsonData)
            user_details = models.User.query.get_by_phone(self.user_phone)
            if not user_details:
                return False

            contact_field_mappings = db.session.query(models.ContactFieldsMapping).all()
            for contact_field_mapping in contact_field_mappings:
                field_name = contact_field_mapping.field_name
                if field_name in jsonData["contact"]["fields"]:
                    field_value = jsonData["contact"]["fields"].get(field_name)
                    if field_value:
                        self.process_contact_fields_data(
                            contact_field_mapping, user_details
                        )
        except Exception as e:
            print(f"Error occurred while handling custom field mapping. Exception: {e}")

    def handle_contact_groups_data(self, jsonData):
        try:
            self.set_init_data(jsonData)
            user_details = models.User.query.get_by_phone(self.user_phone)
            if not user_details:
                return False

            custom_group_mappings = db.session.query(models.ContactFieldsMapping).all()
            for custom_group_mapping in custom_group_mappings:
                for group in jsonData["contact"]["groups"]:
                    if custom_group_mapping.field_name in group["name"]:
                        self.process_contact_groups_data(
                            custom_group_mapping, user_details
                        )
        except Exception as e:
            print(f"Error occurred while handling custom field mapping. Exception: {e}")

    def process_contact_fields_data(self, user_contact_field_details, user_details):
        try:
            table_object = helpers.get_class_by_tablename(
                user_contact_field_details.mapped_table_name
            )
            if table_object:
                column_name = user_contact_field_details.mapped_table_column_name
                mapped_table_column_value = (
                    user_contact_field_details.mapped_table_column_value
                )
                self.update_mapped_fields(
                    table_object,
                    column_name,
                    mapped_table_column_value,
                    user_details,
                )
        except Exception as e:
            print(f"Exception occurred: {e}")

    def process_contact_groups_data(self, user_contact_group_details, user_details):
        try:
            table_object = helpers.get_class_by_tablename(
                user_contact_group_details.mapped_table_name
            )
            if table_object:
                column_name = user_contact_group_details.mapped_table_column_name
                mapped_table_column_value = (
                    user_contact_group_details.mapped_table_column_value
                )
                self.update_mapped_fields(
                    table_object,
                    column_name,
                    mapped_table_column_value,
                    user_details,
                )
        except Exception as e:
            print(f"Exception occurred: {e}")

    def update_mapped_fields(
        self, table_object, column_name, mapped_table_column_value, user_details
    ):
        try:
            table_data = table_object.get_by_user_id(user_details.id)
            if table_data:
                if getattr(table_data, column_name) != mapped_table_column_value:
                    setattr(table_data, column_name, mapped_table_column_value)
                    db.session.commit()
        except Exception as e:
            print(f"Exception occurred: {e}")
