from api import db
from utils.loggingutils import logger
from sqlalchemy import text
from api.helpers import common_helper


def split_the_prompt_by_hyphen(data):
    try:
        split_prompt = data.split("-")
        return split_prompt
    except Exception as e:
        logger.error(
            f"Error while splitting prompt '{data}' by hyphen. Error message: {e}"
        )
        return None


def split_the_prompt_by_underscore(data):
    try:
        program_sub_prompt = data.split("_")
        return program_sub_prompt
    except Exception as e:
        logger.error(
            f"Error while splitting prompt '{data}' by underscore. Error message: {e}"
        )
        return None


def get_program_prompt_id(jsonData):
    """
    Expected program_details categories format (for ex): INTRO_1-SIGNUP_1-SELECTION_PROGRAM-OPTIN_2
    Value returned by this function: 2
    """
    if "program_details" in jsonData:
        program_categories = common_helper.fetch_by_key(
            "categories", jsonData["program_details"]
        )
        if len(program_categories) > 0:
            split_prompt_by_hyphen = split_the_prompt_by_hyphen(program_categories[0])
            split_prompt_by_underscore = split_the_prompt_by_underscore(
                split_prompt_by_hyphen[-1]
            )
            return (
                split_prompt_by_underscore[1]
                if len(split_prompt_by_underscore) > 1
                else None
            )
    return None


def get_column_data_type(table_name, column_name):
    try:
        get_column_type_query = text(
            "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_NAME = :table_name AND COLUMN_NAME = :column_name"
        )
        column_type = db.session.execute(
            get_column_type_query,
            {"table_name": table_name, "column_name": column_name},
        )

        return column_type.fetchone()[0]
    except Exception as e:
        logger.error(
            f"An error occurred while getting data type for column {column_name} in table {table_name}."
            f"Error message: {e}"
        )
        return None
