from __future__ import absolute_import
import json
import pytest
from uuid import uuid4
from random import randint
from faker import Faker
from api.services.transaction_log_service import *
from api.models import *

faker = Faker()

# Load the json payload
payload = json.load(open("tests/payloads/registration_payload.json"))

# Generate a unique flow_run_uuid
new_run_uuid = str(uuid4())

# Insert into the payload
payload["flow_run_details"]["uuid"] = new_run_uuid


def test_create_transaction_log(app, db, setup_test_environment):
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
        transaction_log_instance = TransactionLogService()
        transaction_log_instance.create_new_webhook_log(payload)

        last_transaction_log_record = WebhookTransactionLog.query.get_last_record()
        assert last_transaction_log_record.payload == json.dumps(payload)
