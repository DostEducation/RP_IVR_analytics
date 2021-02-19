# This file is treated as service layer
from api import models, db

def handle_registration(jsonData):
    print("Here we exists")
    try:
        contact = jsonData['contact']
        user_phone = contact['urn']
        print(jsonData['results'])
        registrant = models.Registration(
            user_phone = user_phone.replace("tel:+", ""),
            system_phone='3455456652',
            district='test',
            state='UP',
            status='pending'
        )
        db.session.add(registrant)
        db.session.commit()
    except IndexError:
        print("Failed to register")
