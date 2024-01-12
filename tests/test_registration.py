from __future__ import absolute_import
import json
import pytest
from uuid import uuid4
from random import randint
from faker import Faker
from api.services.registration_service import *
from api.models import *

faker = Faker()

# Load the json payload
payload = json.load(open("tests/payloads/registration_payload.json"))

# Generate a unique flow_run_uuid
new_run_uuid = str(uuid4())

# Insert into the payload
payload["flow_run_details"]["uuid"] = new_run_uuid


def pytest_namespace():
    # We will record the content version from the create operation for future reference
    return {"initial_content_version_id": None}


def test_create_call_log(app, db, setup_test_environment):
    with app.app_context():
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

        # Initialize the registration service.
        registration_service_instance = RegistrationService()
        registration_service_instance.handle_registration(payload)

        user_phone_number = payload["contact"]["urn"].replace("tel:", "")
        registration_model = Registration.query.get_latest_record()
        assert registration_model.user_phone == user_phone_number


def test_update_registration(app, db, setup_test_environment):
    with app.app_context():
        # Initialize the registration service.
        registration_service_instance = RegistrationService()
        registration_service_instance.handle_registration(payload)

        user_phone_number = payload["contact"]["urn"].replace("tel:", "")
        registration_model = Registration.query.get_latest_record()
        assert registration_model.user_phone == user_phone_number
        assert registration_model.has_received_callback == True
