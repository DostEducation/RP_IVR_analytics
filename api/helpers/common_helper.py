def remove_last_string_separated_by(dataString, separator="_"):
    return dataString.rpartition(separator)[0]


def sanitize_phone_string(phoneString):
    """TODO: Need to follow a common guildline throughout the project. Currently Rapid pro and IVR provides phone number in different format"""
    phoneString = phoneString.replace("+", "")
    return phoneString.replace("tel:", "")


def fetch_by_key(key, data):
    """Checks whether a key is present in a json array

    Args:
        key (string): The key which we will be searching for
        data (json): The json array in which we are going to make the search

    Returns:
        string: It will return either string or null if not available
    """
    if key in data:
        return data[key]
    return None


def list_having_string(input_string, list_data):
    """The function checks whether the input string contains one of the list item.
    The list items will act as sub string.

    Args:
        input_string (string): The function will compare the substring against this string.
        list_data (list): The list that contains substrings which will be use to compare.

    Returns:
        [list]: It will returns the list of maching substrings
    """
    return list(filter(lambda x: x in input_string.lower(), list_data))
