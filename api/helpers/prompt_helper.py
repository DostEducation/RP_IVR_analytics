def split_prompt_by_hyphen(data):
    split_prompt = data.split('-')
    return split_prompt

def split_prompt_by_underscore(data):
    program_sub_prompt = data.split('_')
    return program_sub_prompt

def fetch_prompt_response(prompt):
    split_prompt_by_hyphen = helpers.split_prompt_by_hyphen(prompt)
    split_prompt_by_underscore = helpers.split_prompt_by_underscore(split_prompt_by_hyphen[-1])
    return split_prompt_by_underscore[1] if len(split_prompt_by_underscore) > 1 else None
