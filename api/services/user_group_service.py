from api import models, db, helpers


class UserGroupService(object):
    def __init__(self):
        self.user_phone = None

    def handle(self, jsonData):
        user_phone = helpers.fetch_by_key("urn", jsonData["contact"])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        contact_groups = jsonData["contact"]["groups"]
        for group in contact_groups:
            group_data = models.UserGroup.query.get_by_uuid(group["uuid"])
            if group_data:
                self.udpate(group_data)
            else:
                self.add(group)

    def add(self, group):
        user_group_data = models.UserGroup(
            user_id=None,
            registration_id=None,
            user_phone=self.user_phone,
            group_name=group["name"],
            group_uuid=group["uuid"],
            status="active",
        )
        helpers.save(user_group_data)

    def udpate(self, data):
        data.status = "active"
        db.session.commit()
