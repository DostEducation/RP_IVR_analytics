from api import models, db, helpers

# TODO: Need to refactor this and try using ORM
def get_partner_id_by_system_phone(system_phone):
    system_phone_details = models.SystemPhone.query.get_by_phone(system_phone)
    if system_phone_details:
        partner_system_phone = models.PartnerSystemPhone.query.get_by_system_phone_id(
            system_phone_details.id
        )
        if partner_system_phone:
            return partner_system_phone.partner_id
    return None


def get_program_prompt_id(jsonData):
    """
    Expected program_details categories format (for ex): INTRO_1-SIGNUP_1-SELECTION_PROGRAM-OPTIN_2
    Value returned by this function: 2
    """
    if "program_details" in jsonData:
        program_categories = helpers.fetch_by_key(
            "categories", jsonData["program_details"]
        )
        if len(program_categories) > 0:
            split_prompt_by_hyphen = helpers.split_prompt_by_hyphen(
                program_categories[0]
            )
            split_prompt_by_underscore = helpers.split_prompt_by_underscore(
                split_prompt_by_hyphen[-1]
            )
            return (
                split_prompt_by_underscore[1]
                if len(split_prompt_by_underscore) > 1
                else None
            )
    return None


def save(data):
    db.session.add(data)
    db.session.commit()


def get_class_by_tablename(tablename):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for classObject in db.Model._decl_class_registry.values():
        if (
            hasattr(classObject, "__tablename__")
            and classObject.__tablename__ == tablename
        ):
            return classObject
    return None


def save_batch(dataObject):
    db.session.add_all(dataObject)
    db.session.commit()


def get_user_by_phone(phone):
    return models.User.query.get_by_phone(phone)


def get_registrant_by_phone(phone):
    return models.Registration.query.get_latest_by_phone(phone)
