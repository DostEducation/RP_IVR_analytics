# This file is treated as service layer
from api import models, db, helpers
from utils.loggingutils import logger


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
                logger.warning(
                    f"User details not found for the given phone number: {self.user_phone}"
                )
                return False

            for (
                contact_field_mapping
            ) in models.ContactFieldsMapping.query.get_all_contact_fields_mapping():
                field_name = contact_field_mapping.field_name
                if field_name in jsonData["contact"]["fields"]:
                    field_value = jsonData["contact"]["fields"].get(field_name)
                    if field_value:
                        self.process_contact_fields_data(
                            contact_field_mapping, user_details, field_value
                        )
        except Exception as e:
            logger.error(
                f"Error occurred while handling custom field mapping. Exception: {e}"
            )

    def handle_contact_groups_data(self, jsonData):
        try:
            self.set_init_data(jsonData)
            user_details = models.User.query.get_by_phone(self.user_phone)
            if not user_details:
                logger.warning(
                    f"User details not found for the given phone number: {self.user_phone}"
                )
                return False

            for (
                custom_group_mapping
            ) in models.ContactFieldsMapping.query.get_all_contact_fields_mapping():
                for group in jsonData["contact"]["groups"]:
                    if custom_group_mapping.field_name in group["name"]:
                        self.process_contact_groups_data(
                            custom_group_mapping, user_details
                        )
        except Exception as e:
            logger.error(
                f"Error occurred while handling custom field mapping. Exception: {e}"
            )

    def process_contact_fields_data(
        self, user_contact_field_details, user_details, field_value
    ):
        try:
            table_object = helpers.get_class_by_tablename(
                user_contact_field_details.mapped_table_name
            )
            if table_object:
                column_name = user_contact_field_details.mapped_table_column_name
                mapped_table_column_value = (
                    user_contact_field_details.mapped_table_column_value
                )

            if user_contact_field_details.expected_field_data_type.lower() == "boolean":
                if field_value.upper() == "TRUE":
                    mapped_table_column_value = True
                elif field_value.upper() == "FALSE":
                    mapped_table_column_value = False
                else:
                    mapped_table_column_value = None
                    logger.warning("field_value is not a valid boolean value.")

            self.update_mapped_fields(
                table_object,
                column_name,
                mapped_table_column_value,
                user_details,
            )
        except Exception as e:
            logger.error(f"Exception occurred while processing contact field data: {e}")

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
            logger.error(
                f"Exception occurred while processsing contact group data: {e}"
            )

    def update_mapped_fields(
        self, table_object, column_name, mapped_table_column_value, user_details
    ):
        try:
            table_data = table_object.get_by_user_id(user_details.id)
            if table_data:
                if getattr(table_data, column_name) != mapped_table_column_value:
                    setattr(table_data, column_name, mapped_table_column_value)
                    db.session.commit()
                    logger.info(
                        f"Successfully updated {column_name} with value {mapped_table_column_value} for user with id {user_details.id}"
                    )
        except Exception as e:
            logger.error(f"Exception occurred while updating mapped fields: {e}")
