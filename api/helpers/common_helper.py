def get_split_prompt_by_hyphen(data):
    prompt = data['program_details']['categories'][0]
    split_prompt = prompt.split('-')
    return split_prompt

def get_split_prompt_by_underscore(data):
    program_sub_prompt = data.split('_')
    return program_sub_prompt