from api import models, db, services

### Endpoint for Cloud function
def webhook(request):
    if request.method == 'POST':
        try:
            jsonData = request.get_json()
            if 'contact' in jsonData and 'run_uuid' in jsonData and 'flow_category' in jsonData:
                flow_category = jsonData['flow_category']
                # Conditions based on the flow categories
                if flow_category == 'registration':
                    registration = services.RegistrationService()
                    registration.handle_registration(request.json)
                
                # Handle call logs
                calllog = services.CallLogService()
                calllog.handle_call_log(request.json)
                
        except IndexError:
            return jsonify(message="Invalid data"), 400
    return 'Success'
