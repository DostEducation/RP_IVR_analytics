import datetime
from faker import Faker
from api.models import Partner as PartnerInstance
from api import db


class Partner:
    faker = Faker()  # Kept for future use

    def create_partner(self, name, email):
        partner_instance = PartnerInstance()
        partner_instance.name = name
        partner_instance.email = email
        partner_instance.created_on = datetime.datetime.now()

        db.session.add(partner_instance)
        db.session.commit()

        return partner_instance


if __name__ == "__main__":
    seeder = Partner()
    seeder.create_partner(name="UNICEF", email="unicef@test.com")
