from __future__ import absolute_import
import json
import pytest
from uuid import uuid4
from random import randint
from faker import Faker
from api.services.program_sequence_service import *
from api.models import *

faker = Faker()

# Load the json payload
payload = json.load(open("tests/payloads/call_log_payload.json"))

# Generate a unique flow_run_uuid
new_run_uuid = str(uuid4())

# Insert into the payload
payload["flow_run_details"]["uuid"] = new_run_uuid


def test_get_program_sequence(app, db, setup_test_environment):
    with app.app_context():
        # Get a user from User Program
        user_program: UserProgram = UserProgram.query.all()[0]

        # Get a specific user
        user: User = User.query.get_by_id(user_program.user_id)

        # Update user phone number to payload.
        payload["contact"]["urn"] = f"tel:{user.phone}"

        # Get a specific system phone number
        system_phone: SystemPhone = SystemPhone.query.get_by_id(1)

        # Update system phone number to payload.
        payload["channel"]["address"] = f"+91{system_phone.phone}"

        # Get Content Module
        module_content: ModuleContent = ModuleContent.query.all()[0]

        payload["content_id"] = module_content.content_id

        # Initialize the registration service.
        program_sequence_service = ProgramSequenceService()
        sequence_id = program_sequence_service.get_program_sequence_id(payload)

        assert sequence_id != None
