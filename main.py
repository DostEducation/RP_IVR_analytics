from api import services
from flask import jsonify

### Endpoint for Cloud function
def webhook(request):
    if request.method == "POST":
        try:
            jsonData = request.get_json()
            transaction_log_service = services.TransactionLogService()
            webhook_log = transaction_log_service.create_new_webhook_log(jsonData)
            if "contact" in jsonData:
                # Conditions based on the flow categories
                if "flow_category" in jsonData:
                    handle_flow_category_data(jsonData)

                # Handle call logs
                calllog_service = services.CallLogService()
                calllog_service.handle_call_log(jsonData)

                # All the prompt responses are captured with results
                if "results" in jsonData:
                    handle_prompts(jsonData)

                # Handle content details
                user_module_content_id = None
                if "content_id" in jsonData:
                    content_service = services.ContentService()
                    user_module_content_id = content_service.add_user_module_content(
                        jsonData
                    )
                if user_module_content_id:
                    calllog_service.update_user_module_content_id_in_call_log(
                        user_module_content_id
                    )

                # Handle contact groups
                if (
                    "groups" in jsonData["contact"]
                    and jsonData["contact"]["groups"] is not None
                ):
                    user_contact_service = services.UserContactService()
                    user_contact_service.handle_contact_group(jsonData)

                if (
                    "fields" in jsonData["contact"]
                    and jsonData["contact"]["fields"] is not None
                ):
                    user_contact_service = services.UserContactService()
                    user_contact_service.handle_custom_fields(jsonData)

                transaction_log_service.mark_webhook_log_as_processed(webhook_log)
            else:
                return jsonify(message="Contact"), 400
        except IndexError:
            return jsonify(message="Something went wrong!"), 400
        return jsonify(message="Success"), 200
    else:
        return jsonify(message="Currently, the system do not accept a GET request"), 405


def handle_flow_category_data(jsonData):
    registration_service = services.RegistrationService()
    if jsonData["flow_category"] == "registration":
        registration_service.handle_registration(jsonData)


def handle_prompts(jsonData):
    prompt_service = services.PromptService()
    prompt_service.handle_prompt_response(jsonData)
