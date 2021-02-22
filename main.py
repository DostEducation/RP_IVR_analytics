from api import models, db, services

def webhook(request):
    if request.method == 'POST':
        try:
            if len(request.json['contact']) and len(request.json['contact']['flow_category']):
                flow_category = request.json['contact']['flow_category']

                # Conditions based on the flow categories
                if flow_category == 'registration':
                    registration = services.RegistrationService()
                    registration.handle_registration(request.json)
                
        except IndexError:
            print("Failed to update")
    return 'Success'
