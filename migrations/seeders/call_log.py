from faker import Faker
from uuid import uuid4
from api.models import CallLog as CallLogInstance
from api import db


class CallLog:
    faker = Faker()  # Kept for future use

    def create_call_log(self, phone_number, content_id, content_version_id):
        call_log_record = CallLogInstance()
        call_log_record.user_phone_number = phone_number
        call_log_record.content_id = content_id
        call_log_record.content_version_id = content_version_id
        call_log_record.flow_run_uuid = str(uuid4())

        db.session.add(call_log_record)
        db.session.commit()


if __name__ == "__main__":
    seeder = CallLog()
    seeder.create_call_log(
        phone_number="1234567890", content_id=1, content_version_id=1
    )
