from api import models, db, services
from flask import jsonify

### Endpoint for Cloud function
def webhook(request):
    if request.method == 'POST':
        try:
            jsonData = request.get_json()
            if 'contact' in jsonData and 'run_uuid' in jsonData:
                # Conditions based on the flow categories
                if 'flow_category' in jsonData:
                    handle_flow_category_data(jsonData)
                
                # Handle call logs
                calllog_service = services.CallLogService()
                calllog_service.handle_call_log(jsonData)

                # All the prompt responses are captured with results
                if 'results' in jsonData:
                    handle_prompts(jsonData)
            else:
                return jsonify(message = "Contact or Flow Run UUID is missing"), 400
        except IndexError:
            return jsonify(message="Invalid data"), 400
        return jsonify(message = "Success"), 200
    else:
        return jsonify(message = "Currently, the system do not accept a GET request"), 405

def handle_flow_category_data(jsonData):
    registration_service = services.RegistrationService()
    if jsonData['flow_category'] == 'registration':
        registration_service.handle_registration(jsonData)

def handle_prompts(jsonData):
    prompt_service = services.PromptService()
    prompt_service.handle_prompt_response(jsonData)
