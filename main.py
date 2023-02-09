from api import services
from flask import jsonify
from api.helpers import db_helper
from utils.loggingutils import logger
import json

### Endpoint for Cloud function
def webhook(request):
    try:
        if request.method == "POST":
            try:
                jsonData = request.get_json()
            except Exception as e:
                logger.warning("[WARN] Could not retrieve JSON data from the request")
                return jsonify(message="Something went wrong!"), 400

            transaction_log_service = services.TransactionLogService()

            if jsonData and jsonData.get("type", None) != ("retry_failed_log"):
                if "contact" in jsonData:
                    webhook_log = transaction_log_service.create_new_webhook_log(
                        jsonData
                    )
                processed = handle_payload(jsonData)

                if processed is False:
                    logger.error("[ERROR] Error processing the payload")
                    return jsonify(message="Something went wrong!"), 400
                elif processed == -1:
                    logger.warning("[ERROR] Contact not found in the payload")
                    return jsonify(message="Contact"), 400

                if "contact" in jsonData:
                    transaction_log_service.mark_webhook_log_as_processed(webhook_log)
            elif jsonData and jsonData.get("type", None) == "retry_failed_log":
                retry_failed_webhook(transaction_log_service)

            return jsonify(message="Success"), 200
        else:
            logger.warning("[WARN] Received a GET request instead of POST")
            return (
                jsonify(message="Currently, the system do not accept a GET request"),
                405,
            )
    except Exception as e:
        logger.error("[ERROR] An unexpected error occurred: %s" % e)
        return jsonify(message="Internal server error"), 500


def retry_failed_webhook(transaction_log_service):
    failed_webhook_logs = transaction_log_service.get_failed_webhook_transaction_log()

    for log in failed_webhook_logs:
        log.attempts += 1
        db_helper.save(log)

        json_data = json.loads(log.payload)
        json_data["log_created_on"] = log.created_on
        processed = handle_payload(json_data, True)

        if processed is not True:
            continue

        log.processed = True
        db_helper.save(log)
        logger.info("[INFO] Successfully processed the failed log")


def handle_payload(jsonData, is_retry_payload=False):
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
            program_sequence_id = None

            if "content_id" in jsonData:
                program_sequence_service = services.ProgramSequenceService()
                (
                    program_sequence_id
                ) = program_sequence_service.get_program_sequence_id(jsonData)

                if program_sequence_id:
                    calllog_service.update_program_sequence_id_in_call_log(
                        program_sequence_id
                    )

            # Handle contact groups
            if (
                "groups" in jsonData["contact"]
                and jsonData["contact"]["groups"] is not None
                and jsonData.get("flow_category", None) == "dry_flow"
                and not is_retry_payload
            ):
                handle_user_group_data(jsonData)

            # Handle custom fields
            if (
                "fields" in jsonData["contact"]
                and jsonData["contact"]["fields"] is not None
                and jsonData.get("flow_category", None) == "dry_flow"
                and not is_retry_payload
            ):
                handle_user_custom_field_data(jsonData)

            # Handle groups and fields
            if jsonData.get("flow_category") == "dry_flow" and not is_retry_payload:
                handle_contact_fields_and_groups(jsonData)
        else:
            logger.error("[ERROR] No 'contact' key found in the input JSON data.")
            return -1
    except Exception as e:
        logger.error("[ERROR] Exception Occured: %s" % e)
        return False
    logger.info("[INFO] Payload processing completed successfully.")
    return True


def handle_flow_category_data(jsonData):
    registration_service = services.RegistrationService()
    try:
        if jsonData["flow_category"] == "registration":
            registration_service.handle_registration(jsonData)
    except Exception as e:
        logger.error(f"Error occurred in handle_registration: {e}")


def handle_user_group_data(jsonData):
    user_contact_service = services.UserContactService()
    try:
        user_contact_service.handle_contact_group(jsonData)
    except Exception as e:
        logger.error(f"Error occurred in handle_contact_group: {e}")


def handle_user_custom_field_data(jsonData):
    user_contact_service = services.UserContactService()
    try:
        user_contact_service.handle_custom_fields(jsonData)
    except Exception as e:
        logger.error(f"Error occurred in handle_custom_fields: {e}")


def handle_prompts(jsonData):
    prompt_service = services.PromptService()
    try:
        prompt_service.handle_prompt_response(jsonData)
    except Exception as e:
        logger.error(f"Error occurred in handle_prompt_response: {e}")


def handle_contact_fields_and_groups(JsonData):
    custom_fields_mapping_service = services.ContactFieldsMappingService()
    try:
        contact_data = JsonData["contact"]
        if contact_data.get("fields"):
            custom_fields_mapping_service.handle_contact_fields_data(JsonData)
    except Exception as e:
        logger.error(f"Error occurred in handle_contact_fields_data: {e}")

    try:
        if contact_data.get("groups"):
            custom_fields_mapping_service.handle_contact_groups_data(JsonData)
    except Exception as e:
        logger.error(f"Error occurred in handle_contact_groups_data: {e}")
