def get_split_prompt_by_hyphen(data):
    split_prompt = data.split('-')
    return split_prompt

def get_split_prompt_by_underscore(data):
    program_sub_prompt = data.split('_')
    return program_sub_prompt

def remove_last_string_separated_by(dataString, separator = '_'):
    return dataString.rpartition(separator)[0]

def sanitize_phone_string(phoneString):
	return phoneString.replace("tel:", "")

def fetch_by_key(key, data):
    if key in data:
        return data[key]
    return None
