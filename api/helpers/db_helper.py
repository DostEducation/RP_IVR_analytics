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
