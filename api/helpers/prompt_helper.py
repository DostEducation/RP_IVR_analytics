from api import helpers


def split_prompt_by_hyphen(data):
    split_prompt = data.split("-")
    return split_prompt


def split_prompt_by_underscore(data):
    program_sub_prompt = data.split("_")
    return program_sub_prompt


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


def get_time_selection(jsonData):
    """
    Expected time categories format (for ex): INTRO_1-SIGNUP_1-SELECTION_TIME-OPTIN_MORNING
    """
    if "results" in jsonData:
        time_categories = helpers.fetch_by_key(
            "intro_1_signup_1_selection_time_optin", jsonData["results"]
        )
        if time_categories:
            split_prompt_by_hyphen = helpers.split_prompt_by_hyphen(
                time_categories["category"]
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
