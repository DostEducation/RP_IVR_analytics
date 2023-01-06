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

            custom_fields = jsonData["contact"]["fields"]

            if custom_fields:
                for key in custom_fields:
                    field_value = custom_fields[key]
                    if key in custom_fields and field_value:
                        field_name = key
                        user_contact_field_details = (
                            models.ContactFieldsMapping.query.get_by_field_name(
                                field_name, field_value
                            )
                        )
                        if user_contact_field_details:
                            self.process_contact_fields_data(
                                user_contact_field_details, user_details
                            )
        except Exception as e:
            print(f"Exception occurred: {e}")

    def handle_contact_groups_data(self, jsonData):
        try:
            self.set_init_data(jsonData)
            user_details = models.User.query.get_by_phone(self.user_phone)
            if not user_details:
                return False

            contact_groups = jsonData["contact"]["groups"]

            if contact_groups:
                for contact_group in contact_groups:
                    contact_group_name = contact_group["name"]
                    user_contact_group_details = (
                        models.ContactFieldsMapping.query.get_by_group_name(
                            contact_group_name
                        )
                    )
                    if user_contact_group_details:
                        self.process_contact_groups_data(
                            user_contact_group_details, user_details
                        )
        except Exception as e:
            print(f"Exception occurred: {e}")

    def process_contact_fields_data(self, user_contact_field_details, user_details):
        try:
            for user_contact_field_detail in user_contact_field_details:
                class_object = helpers.get_class_by_tablename(
                    user_contact_field_detail.mapped_table_name
                )
                if class_object:
                    column_name = user_contact_field_detail.mapped_table_column_name
                    mapped_table_column_value = (
                        user_contact_field_detail.mapped_table_column_value
                    )
                    self.update_mapped_fields(
                        class_object,
                        column_name,
                        mapped_table_column_value,
                        user_details,
                    )
        except Exception as e:
            print(f"Exception occurred: {e}")

    def process_contact_groups_data(self, user_contact_group_details, user_details):
        try:
            for user_contact_group_detail in user_contact_group_details:
                class_object = helpers.get_class_by_tablename(
                    user_contact_group_detail.mapped_table_name
                )
                if class_object:
                    column_name = user_contact_group_detail.mapped_table_column_name
                    mapped_table_column_value = (
                        user_contact_group_detail.mapped_table_column_value
                    )
                    self.update_mapped_fields(
                        class_object,
                        column_name,
                        mapped_table_column_value,
                        user_details,
                    )
        except Exception as e:
            print(f"Exception occurred: {e}")

    def update_mapped_fields(
        self, class_object, column_name, mapped_table_column_value, user_details
    ):
        try:
            class_object_data = class_object.get_by_user_id(user_details.id)
            if class_object_data:
                setattr(class_object, column_name, mapped_table_column_value)
                db.session.commit()
        except Exception as e:
            print(f"Exception occurred: {e}")
