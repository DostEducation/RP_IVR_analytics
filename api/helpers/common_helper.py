def remove_last_string_separated_by(dataString, separator = '_'):
    return dataString.rpartition(separator)[0]

def sanitize_phone_string(phoneString):
	""" TODO: Need to follow a common guildline throughout the project. Currently Rapid pro and IVR provides phone number in different format"""
	phoneString = phoneString.replace("+", "")
	return phoneString.replace("tel:", "")

def fetch_by_key(key, data):
    if key in data:
        return data[key]
    return None
