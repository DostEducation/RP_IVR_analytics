from flask import jsonify
from api import app, helpers, services, models
from utils.loggingutils import logger
import json

user_program_service = services.UserProgramService()

### Endpoint for Cloud function
def webhook(request):
    with app.app_context():
        try:
            if request.method == "POST":
                try:
                    jsonData = request.get_json()
                except Exception as e:
                    logger.warning(
                        f"[WARN] Could not retrieve JSON data from the request. Error:{e}"
                    )
                    return jsonify(message="Something went wrong!"), 400

                if jsonData.get("flow_category", None) == "dry_flow":
                    handle_dry_flow(jsonData)
                else:
                    handle_regular_flow(jsonData)
                return jsonify(message="Success"), 200

            logger.warning("[WARN] Received a GET request instead of POST")
            return (
                jsonify(message="Currently, the system does not accept a GET request"),
                405,
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred. Error message: {e}")
            return jsonify(message="Internal server error"), 500


def handle_dry_flow(jsonData):
    # Handle contact groups
    if "groups" in jsonData["contact"] and jsonData["contact"]["groups"] is not None:
        if jsonData.get("churned", None) is True:
            user_program_service.update_user_program_status(
                jsonData, status=models.UserProgram.UserProgramStatus.TERMINATED
            )


def handle_regular_flow(jsonData):
    transaction_log_service = services.TransactionLogService()
    if jsonData and jsonData.get("type", None) == "retry_failed_log":
        retry_failed_webhook(transaction_log_service)
    else:
        if "contact" in jsonData:
            webhook_log = transaction_log_service.create_new_webhook_log(jsonData)
        processed = handle_payload(jsonData)

        if processed is False:
            logger.error(f"Error processing the payload: {jsonData}")
            return jsonify(message="Something went wrong!"), 400
        if processed == -1:
            logger.warning("Contact not found in the payload")
            return jsonify(message="Contact"), 400

        if "contact" in jsonData:
            transaction_log_service.mark_webhook_log_as_processed(webhook_log)
    return None


def retry_failed_webhook(transaction_log_service):
    failed_webhook_logs = transaction_log_service.get_failed_webhook_transaction_log()

    for log in failed_webhook_logs:
        log.attempts += 1
        helpers.db_helper.save(log)

        json_data = json.loads(log.payload)
        json_data["log_created_on"] = log.created_on
        processed = handle_payload(json_data)
        if processed is not True:
            continue

        log.processed = True
        helpers.db_helper.save(log)


def handle_payload(jsonData):
    try:
        if "contact" in jsonData:
            # Conditions based on the flow categories
            if "flow_category" in jsonData:
                handle_flow_category_data(jsonData)
                # Handle call logs
                calllog_service = services.CallLogService()
                calllog_service.handle_call_log(jsonData)

            if jsonData.get("is_last_content", None) is True:
                user_program_service.update_user_program_status(
                    jsonData, status=models.UserProgram.UserProgramStatus.COMPLETE
                )

            if jsonData.get("unsub", None) is True:
                user_program_service.update_user_program_status(
                    jsonData, status=models.UserProgram.UserProgramStatus.UNSUB
                )

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
        else:
            logger.error(f"No 'contact' key found in the input JSON data. {jsonData}")
            return -1
    except Exception as e:
        logger.error(f"Exception occurred while handling payload: {e}")
        return False
    return True


def handle_flow_category_data(jsonData):
    registration_service = services.RegistrationService()
    if jsonData["flow_category"] == "registration":
        registration_service.handle_registration(jsonData)


def handle_prompts(jsonData):
    prompt_service = services.PromptService()
    prompt_service.handle_prompt_response(jsonData)
