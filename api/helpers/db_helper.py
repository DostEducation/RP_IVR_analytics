from api import models, db
import traceback
from utils.loggingutils import logger

# TODO: Need to refactor this and try using ORM
def get_partner_id_by_system_phone(system_phone):
    try:
        system_phone_details = models.SystemPhone.query.get_by_phone(system_phone)
        if system_phone_details:
            partner_system_phone = (
                models.PartnerSystemPhone.query.get_by_system_phone_id(
                    system_phone_details.id
                )
            )
            if partner_system_phone:
                return partner_system_phone.partner_id
    except Exception as e:
        logger.error(f"Error while fetching partner id by system phone: {e}")
    return None


def save(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        logger.error(
            f"Error occurred while processing the webhook. Error Message:  {e}"
        )
        logger.debug(traceback.format_exc())
        db.session.rollback()


def get_class_by_tablename(tablename):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    logger.info("Searching for class mapped to table '%s'", tablename)
    for classObject in db.Model._decl_class_registry.values():
        if (
            hasattr(classObject, "__tablename__")
            and classObject.__tablename__ == tablename
        ):
            logger.info(
                "Found class '%s' mapped to table '%s'", classObject.__name__, tablename
            )
            return classObject
    logger.warning("No class found mapped to table '%s'", tablename)
    return None


def save_batch(dataObject):
    try:
        db.session.add_all(dataObject)
        db.session.commit()
        logger.info(f"Data object batch saved successfully: {dataObject}")
    except Exception as e:
        logger.error(f"Error occurred while saving data object batch: {e}")


def get_user_by_phone(phone):
    try:
        return models.User.query.get_by_phone(phone)
    except Exception as e:
        logger.error(
            f"Error occurred while fetching user for phone number: {phone}. Error: {e}"
        )
        return None


def get_registrant_by_phone(phone):
    try:
        return models.Registration.query.get_latest_by_phone(phone)
    except Exception as e:
        logger.error(
            f"Error occurred while fetching registrant for phone number: {phone}. Error: {e}"
        )
        return None
