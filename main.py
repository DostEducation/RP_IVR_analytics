from api import services, models, db

def webhook(request):
    if request.method == 'POST':
        try:
            if (request.json['contact'] and request.json['contact']['flow_category']):
                services.handle_registration(request.json)
        except IndexError:
            print("Failed to update")
    return 'Success'
