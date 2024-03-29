from __future__ import absolute_import
import json
import pytest
from faker import Faker
from api.services.prompt_service import *
from api.models import *
from api import db

faker = Faker()

# Load the json payload
payload = json.load(open("tests/payloads/registration_payload.json"))


def pytest_namespace():
    # We will record the content version from the create operation for future reference
    return {"initial_content_version_id": None}


def test_prompt_response(app, db, setup_test_environment):
    with app.app_context():
        # Get call log record
        call_log: CallLog = CallLog.query.all()[0]

        # Get a specific user
        user: User = User.query.get_by_phone(call_log.user_phone_number)

        # Insert into the payload
        payload["flow_run_details"]["uuid"] = call_log.flow_run_uuid

        # Update user phone number to payload.
        payload["contact"]["urn"] = f"tel:{user.phone}"

        # Get a specific system phone number
        system_phone: SystemPhone = SystemPhone.query.get_by_id(1)

        # Update system phone number to payload.
        payload["channel"]["address"] = f"+91{system_phone.phone}"

        # Get a specific content
        content_version: ContentVersion = ContentVersion.query.get_by_id(
            call_log.content_version_id
        )

        payload["content_id"] = content_version.content_id
        payload["language_id"] = content_version.language_id

        # Initialize the Prompt service.
        prompt_service_instance = PromptService()
        prompt_service_instance.handle_prompt_response(payload)

        user_phone_number = (
            payload["contact"]["urn"].replace("tel:", "").replace("+", "")
        )
        ivr_prompt_response = IvrPromptResponse.query.get_latest_prompt()
        assert ivr_prompt_response.user_phone == user_phone_number
