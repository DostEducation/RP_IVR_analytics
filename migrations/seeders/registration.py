from faker import Faker
from api.models import Registration as RegistrationModel
from api import db


class Registration:
    faker = Faker()

    def create_registration(
        self, user_phone_number, system_phone_number, partner_id, user_id
    ):
        registration = RegistrationModel()
        registration.user_id = user_id
        registration.user_phone = user_phone_number
        registration.system_phone = system_phone_number
        registration.partner_id = partner_id

        db.session.add(registration)
        db.session.commit()


if __name__ == "__main__":
    seeder = Registration()
    seeder.create_registration(
        user_phone_number="+911234567890",
        system_phone_number="9876543210",
        partner_id=1,
        user_id=1,
    )
