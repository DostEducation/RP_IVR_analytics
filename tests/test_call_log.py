from __future__ import absolute_import
import json
import pytest
from uuid import uuid4
from random import randint
from faker import Faker
from api.services.call_log_service import *
from api.models import *

faker = Faker()

# Load the json payload
payload = json.load(open("tests/payloads/call_log_payload.json"))

# Generate a unique flow_run_uuid
new_run_uuid = str(uuid4())

# Insert into the payload
payload["flow_run_details"]["uuid"] = new_run_uuid


def pytest_namespace():
    # We will record the content version from the create operation for future reference
    return {"initial_content_version_id": None}


def test_create_call_log(app, db, setup_test_environment):
    # Get a specific user
    user: User = User.query.get_by_id(1)

    # Update user phone number to payload.
    payload["contact"]["urn"] = f"tel:{user.phone}"

    # Get a specific system phone number
    system_phone: SystemPhone = SystemPhone.query.get_by_id(1)

    # Update system phone number to payload.
    payload["channel"]["address"] = f"+91{system_phone.phone}"

    # Get a specific content
    content_version: ContentVersion = ContentVersion.query.get_by_id(1)

    payload["content_id"] = content_version.content_id
    payload["language_id"] = content_version.language_id

    # Initialize the call log service.
    call_log_service_instance = CallLogService()
    call_log_service_instance.handle_call_log(payload)

    call_log_model = CallLog.query.get_by_flow_run_uuid(new_run_uuid)
    pytest.initial_content_version_id = call_log_model.content_version_id
    assert call_log_model != None


def test_update_call_log(app, db, setup_test_environment):
    # Get all content version records
    all_content_version_records = ContentVersion.query.all()

    stop_iteration = False
    new_content_id = None
    new_language_id = None
    while not stop_iteration:
        random_index = randint(0, len(all_content_version_records))
        if (
            all_content_version_records[random_index].id
            != pytest.initial_content_version_id
        ):
            new_content_id = all_content_version_records[random_index].content_id
            new_language_id = all_content_version_records[random_index].language_id
            stop_iteration = True

    payload["content_id"] = new_content_id
    payload["contact"]["fields"]["language_id"] = new_language_id

    # Initialize the call log service.
    call_log_service_instance = CallLogService()
    call_log_service_instance.handle_call_log(payload)

    call_log_model = CallLog.query.get_by_flow_run_uuid(new_run_uuid)
    assert call_log_model.content_version_id != pytest.initial_content_version_id
