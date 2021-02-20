# This file is treated as service layer
from api import models, db

### Main function, used to getting called from cloud function
def handle_registration(jsonData):
    try:
        contact = jsonData['contact']
        user_phone = contact['urn']
        register(user_phone, jsonData)
        # add_prompt_response(user_phone, jsonData)

    except IndexError:
        print("Failed to register")


def register(user_phone, jsonData):
    system_phone = jsonData['system_phone']
    system_phone_details = models.SystemPhone.query.get_by_phone(system_phone)
    split_prompt_by_hyphen = get_split_prompt_by_hyphen(jsonData)
    split_prompt_by_underscore = get_split_prompt_by_underscore(split_prompt_by_hyphen[-1])
    if system_phone_details:
        registrant_state = system_phone_details.state
        registrant = models.Registration(
            user_phone = user_phone.replace("tel:+", ""),
            system_phone = system_phone,
            state = registrant_state,
            status ='Pending',
            program_id = split_prompt_by_underscore[1]
        )
        db.session.add(registrant)
        db.session.commit()

def add_prompt_response(user_phone, jsonData):
    # to capture prompt response

def get_split_prompt_by_hyphen(data):
    prompt = data['program_details']['categories'][0]
    split_prompt = prompt.split('-')
    return split_prompt

def get_split_prompt_by_underscore(data):
    program_sub_prompt = data.split('_')
    return program_sub_prompt