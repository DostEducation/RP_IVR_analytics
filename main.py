from api import models, db, services

def webhook(request):
    if request.method == 'POST':
        try:
            if (request.json['contact'] and request.json['contact']['flow_category']):
                print('Before handle registration function')
                registration = services.RegistrationService()
                registration.handle_registration(request.json)
        except IndexError:
            print("Failed to update")
    return 'Success'
