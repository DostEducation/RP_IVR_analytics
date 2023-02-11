# This file is treated as service layer
from api import models, db, helpers
from utils.loggingutils import logger


class UserContactService(object):
    def __init__(self):
        self.user_phone = None
        self.user_data = None
        self.registration_data = None
        self.flow_run_uuid = None
        self.custom_field_prefix = "dost"

    def init_data(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        self.user_data = helpers.get_user_by_phone(self.user_phone)
        self.registration_data = helpers.get_registrant_by_phone(self.user_phone)
        self.flow_run_uuid = helpers.fetch_by_key(
            "run_uuid", jsonData
        )  # Need to remove once we are done with making changes in webhooks
        if "flow_run_details" in jsonData:
            self.flow_run_uuid = helpers.fetch_by_key(
                "uuid", jsonData["flow_run_details"]
            )

    def handle_contact_group(self, jsonData):
        try:
            self.init_data(jsonData)
            contact_groups = jsonData["contact"]["groups"]
            user_groups = models.UserGroup.query.get_by_user_phone(self.user_phone)
            active_user_group_uuid_list = {}

            for user_group in user_groups:
                active_user_group_uuid_list[
                    str(user_group.group_uuid)
                ] = models.UserGroup.UserGroupStatus.ACTIVE

            for group in contact_groups:
                group_data = models.UserGroup.query.get_unique(
                    group["uuid"], self.user_phone
                )
                if (
                    group_data
                    and group_data.status == models.UserGroup.UserGroupStatus.INACTIVE
                ):
                    self.update_group(group_data)
                elif not group_data:
                    self.add_group(group)

                if group["uuid"] in active_user_group_uuid_list:
                    active_user_group_uuid_list.pop(group["uuid"])

            for group_uuid in active_user_group_uuid_list:
                self.mark_user_groups_as_inactive(group_uuid)
        except Exception as e:
            logger.error(
                f"Failed to handle contact group data for {self.user_phone}. Error: {e}"
            )

    def add_group(self, group):
        try:
            user_group_data = models.UserGroup(
                user_id=self.user_data.id if self.user_data else None,
                registration_id=self.registration_data.id
                if self.registration_data
                else None,
                user_phone=self.user_phone,
                group_name=group["name"],
                group_uuid=group["uuid"],
                status=models.UserGroup.UserGroupStatus.ACTIVE,
            )
            helpers.save(user_group_data)
        except Exception as e:
            logger.error(
                f"Failed to add group for user phone {self.user_phone}: {group['name']}. Error: {e}"
            )

    def update_group(self, data):
        data.status = models.UserGroup.UserGroupStatus.ACTIVE
        try:
            db.session.commit()
        except Exception as e:
            logger.error(
                f"Failed to update group for user phone {self.user_phone}: {data.group_name}. Error: {str(e)}"
            )

    def handle_custom_fields(self, jsonData):
        """Handle contact custom fields data
        Args:
            jsonData (json): json data we are getting from webhook
        """
        try:
            self.init_data(jsonData)
            user_custom_field_data = models.UserCustomFields.query.get_by_user_phone(
                self.user_phone
            )

            self.process_custom_fields(jsonData, user_custom_field_data)
        except Exception as e:
            logger.error(
                f"Failed to handle custom fields for user phone {self.user_phone}. Error: {e}"
            )

    def process_custom_fields(self, jsonData, user_custom_field_data=False):
        try:
            custom_fields = jsonData["contact"]["fields"]
            fields_key_values = {}
            active_custom_fields_data = self.get_active_custom_fields(
                user_custom_field_data
            )
            active_custom_fields_key_values = {}

            if active_custom_fields_data:
                active_custom_fields_key_values = self.fetch_fields_key_value(
                    active_custom_fields_data
                )

            if user_custom_field_data:
                fields_key_values = self.fetch_fields_key_value(user_custom_field_data)

            user_custom_contact_data = []

            for field_name, field_value in custom_fields.items():
                custom_fields_conditions = self.custom_fields_conditions(
                    field_name, field_value
                )

                if (
                    custom_fields_conditions
                    and self.check_if_exist(fields_key_values, field_name, field_value)
                    == False
                ):
                    userdata = self.get_user_custom_fields_object(
                        field_name, field_value
                    )
                    user_custom_contact_data.extend(userdata)
                elif custom_fields_conditions and not self.check_if_exist(
                    active_custom_fields_key_values, field_name, field_value
                ):
                    models.UserCustomFields.query.set_custom_field_as_active(
                        field_name, field_value, self.user_phone
                    )
                elif custom_fields_conditions and self.check_if_exist(
                    active_custom_fields_key_values, field_name, field_value
                ):
                    active_custom_fields_key_values.pop(
                        str(field_name) + "_" + str(field_value)
                    )

            for (
                custom_field_name,
                custom_field_value,
            ) in active_custom_fields_key_values.items():
                custom_field_key = custom_field_name[: -(len(custom_field_value) + 1)]
                models.UserCustomFields.query.set_custom_field_as_inactive(
                    self.user_phone, custom_field_key, custom_field_value
                )

            if user_custom_contact_data:
                helpers.save_batch(user_custom_contact_data)
        except Exception as e:
            logger.error(
                f"Failed to process custom fields for user phone {self.user_phone}. Error: {e}"
            )

    def fetch_fields_key_value(self, user_custom_field_data):
        """Format the existing fields in key value pair
        Args:
            user_custom_field_data (model object): It is user custom field data model object we are getting on running query.
        Returns:
            dict: Dictionary
        """

        data_list = {}
        for data in user_custom_field_data:
            try:
                data_list[
                    str(data.field_name) + "_" + str(data.field_value)
                ] = data.field_value
            except Exception as e:
                logger.error(
                    f"Error while fetching key values for user phone {self.user_phone}. Error: {e}"
                )
        return data_list

    def check_if_exist(self, fields_key_values, field_name, field_value):
        """This function is use to check whether the field name and it's similar value already exists in database or not.
        As there can be multiple entries for same field name, using field name and field value as index

        Args:
            fields_key_values (dict): Dictionary we are getting from fetch_fields_key_value
            field_name (str): custom field name
            field_value (str)): custom field value

        Returns:
            [bool]: Returns whether the field name and value exists.
        """
        #
        key_index = str(field_name) + "_" + str(field_value)
        return (
            True
            if (
                fields_key_values
                and key_index in fields_key_values
                and field_value == fields_key_values[key_index]
            )
            else False
        )

    def get_user_custom_fields_object(self, field_name, field_value):
        return [
            models.UserCustomFields(
                user_id=self.user_data.id if self.user_data else None,
                registration_id=self.registration_data.id
                if self.registration_data
                else None,
                user_phone=self.user_phone,
                field_name=field_name,
                field_value=field_value,
                flow_run_uuid=self.flow_run_uuid,
                status=models.UserCustomFields.UserCustomFieldStatus.ACTIVE,
            ),
        ]

    def custom_fields_conditions(self, field_name, field_value):
        return (
            True
            if field_value is not None
            and field_name.startswith(self.custom_field_prefix)
            else False
        )

    def mark_user_groups_as_inactive(self, group_uuid):
        try:
            models.UserGroup.query.mark_user_groups_as_inactive(
                self.user_phone, group_uuid
            )
            db.session.commit()
        except Exception as e:
            logger.error(
                f"Error while marking user groups as inactive for {self.user_phone}. Error:{e}"
            )

    def get_active_custom_fields(self, user_custom_field_data):
        try:
            if user_custom_field_data:
                return [
                    data
                    for data in user_custom_field_data
                    if data.status
                    == models.UserCustomFields.UserCustomFieldStatus.ACTIVE
                ]
        except Exception as e:
            logger.error(
                f"Failed to get active custom fields for {self.user_phone}. Error:{e}"
            )
