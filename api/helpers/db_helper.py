from api import db
import traceback
from utils.loggingutils import logger


def save(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        logger.error(
            f"Error occurred while committing the data in the database. Error message: {e}"
        )
        logger.debug(traceback.format_exc())
        db.session.rollback()


def get_class_by_tablename(tablename):
    """Return class reference mapped to table.
    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for classObject in db.Model.registry._class_registry.values():
        if (
            hasattr(classObject, "__tablename__")
            and classObject.__tablename__ == tablename
        ):
            return classObject
    return None


def save_batch(dataObject):
    try:
        db.session.add_all(dataObject)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error occurred while saving data object batch: {e}")
