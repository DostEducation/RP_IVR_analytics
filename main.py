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
                    registration_service = services.RegistrationService()
                    registration_service.handle_registration(jsonData)
                
                # Handle call logs
                calllog_service = services.CallLogService()
                calllog_service.handle_call_log(jsonData)

                # All the prompt responses are captured with results
                if 'results' in jsonData:
                    prompt_service = services.PromptService()
                    prompt_service.add_prompt_response(jsonData)
                
        except IndexError:
            return jsonify(message="Invalid data"), 400
    return 'Success'
