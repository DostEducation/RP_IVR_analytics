from api import models, db, helpers


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
        self.init_data(jsonData)
        contact_groups = jsonData["contact"]["groups"]
        if contact_groups:
            models.UserGroup.query.inactivate(self.user_phone)
            for group in contact_groups:
                group_data = models.UserGroup.query.get_unique(
                    group["uuid"], self.user_phone
                )
                if group_data:
                    self.udpate_group(group_data)
                else:
                    self.add_group(group)

    def add_group(self, group):
        user_group_data = models.UserGroup(
            user_id=self.user_data.id if self.user_data else None,
            registration_id=self.registration_data.id
            if self.registration_data
            else None,
            user_phone=self.user_phone,
            group_name=group["name"],
            group_uuid=group["uuid"],
            status="active",
        )
        helpers.save(user_group_data)

    def udpate_group(self, data):
        data.status = "active"
        db.session.commit()

    def handle_custom_fields(self, jsonData):
        """Handle contact custom fields data
        Args:
            jsonData (json): json data we are getting from webhook
        """
        self.init_data(jsonData)
        user_custom_field_data = models.UserCustomFields.query.get_by_user_phone(
            self.user_phone
        )
        self.process_custom_fields(jsonData, user_custom_field_data)

    def process_custom_fields(self, jsonData, user_custom_field_data=False):
        custom_fields = jsonData["contact"]["fields"]
        fields_key_values = {}
        if user_custom_field_data:
            fields_key_values = self.fetch_fields_key_value(user_custom_field_data)
        user_custom_contact_data = []
        for field_name, field_value in custom_fields.items():
            custom_fields_conditions = self.custom_fields_contidions(
                field_name, field_value
            )
            if (
                custom_fields_conditions
                and self.check_if_exist(fields_key_values, field_name, field_value)
                == False
            ):
                userdata = self.get_user_custom_fields_object(field_name, field_value)
                user_custom_contact_data.extend(userdata)

        if user_custom_contact_data:
            helpers.save_batch(user_custom_contact_data)

    def fetch_fields_key_value(self, user_custom_field_data):
        """Format the existing fields in key value pair
        Args:
            user_custom_field_data (model object): It is user custom field data model object we are getting on running query.
        Returns:
            dict: Dictionary
        """

        data_list = {}
        for data in user_custom_field_data:
            data_list[
                str(data.field_name) + "_" + str(data.field_value)
            ] = data.field_value
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
            ),
        ]

    def custom_fields_contidions(self, field_name, field_value):
        return (
            True
            if field_value is not None
            and field_name.startswith(self.custom_field_prefix)
            else False
        )
