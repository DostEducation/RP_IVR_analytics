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

    def custom_fields_contidions(self, field_name, field_value):
        return (
            True
            if field_value is not None
            and field_name.startswith(self.custom_field_prefix)
            else False
        )
