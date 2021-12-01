from api import services
from flask import jsonify
import json

from api.helpers import db_helper

### Endpoint for Cloud function
def webhook(request):
    if request.method == "POST":
        try:
            jsonData = request.get_json()
        except:
            return jsonify(message="Something went wrong!"), 400

        transaction_log_service = services.TransactionLogService()

        if jsonData and jsonData.get("type", None) != ("retry_failed_log"):
            if "contact" in jsonData:
                webhook_log = transaction_log_service.create_new_webhook_log(jsonData)
            processed = handle_payload(jsonData)

            if processed is False:
                return jsonify(message="Something went wrong!"), 400
            elif processed == -1:
                return jsonify(message="Contact"), 400

            if "contact" in jsonData:
                transaction_log_service.mark_webhook_log_as_processed(webhook_log)
        elif jsonData and jsonData.get("type", None) == "retry_failed_log":
            retry_failed_webhook(transaction_log_service)

        return jsonify(message="Success"), 200
    else:
        return jsonify(message="Currently, the system do not accept a GET request"), 405


def retry_failed_webhook(transaction_log_service):
    failed_webhook_logs = transaction_log_service.get_failed_webhook_transaction_log()

    for log in failed_webhook_logs:
        processed = handle_payload(json.loads(log.payload))

        if processed is not True:
            continue

        log.processed = True
        db_helper.save(log)


def handle_payload(jsonData):
    try:
        if "contact" in jsonData:
            # Conditions based on the flow categories
            if "flow_category" in jsonData and jsonData["flow_category"] != "dry_flow":
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
                and jsonData.get("flow_category", None) == "dry_flow"
            ):
                handle_user_group_data(jsonData)

            # Handle custom fields
            if (
                "fields" in jsonData["contact"]
                and jsonData["contact"]["fields"] is not None
                and jsonData.get("flow_category", None) == "dry_flow"
            ):
                handle_user_custom_field_data(jsonData)
        else:
            return -1
    except:
        return False
    return True


def handle_flow_category_data(jsonData):
    registration_service = services.RegistrationService()
    if jsonData["flow_category"] == "registration":
        registration_service.handle_registration(jsonData)


def handle_user_group_data(jsonData):
    user_contact_service = services.UserContactService()
    user_contact_service.handle_contact_group(jsonData)


def handle_user_custom_field_data(jsonData):
    user_contact_service = services.UserContactService()
    user_contact_service.handle_custom_fields(jsonData)


def handle_prompts(jsonData):
    prompt_service = services.PromptService()
    prompt_service.handle_prompt_response(jsonData)
