from faker import Faker
from api.models import SystemPhone as SystemPhoneModel
from random import randint
from api import db
from typing import List
import datetime


class SystemPhone:
    faker = Faker()

    def generate_random_phone_numbers(self):
        return randint(1000000000, 9999999999)

    def create_system_phone(self, count=10) -> List:
        already_used_phone_numbers = set({})
        system_phone_instances = []

        for _ in range(count):
            search_new_phone_number = True
            current_phone_number = None
            while search_new_phone_number:
                new_phone_number = self.generate_random_phone_numbers()
                if not new_phone_number in already_used_phone_numbers:
                    current_phone_number = new_phone_number
                    already_used_phone_numbers.add(new_phone_number)
                    search_new_phone_number = False

            system_phone_instance = SystemPhoneModel()
            system_phone_instance.phone = current_phone_number
            system_phone_instance.state = "MP"
            system_phone_instance.status = "active"
            system_phone_instance.created_on = datetime.datetime.now()

            system_phone_instances.append(system_phone_instance)

        # Store to database
        db.session.add_all(system_phone_instances)
        db.session.commit()

        return [str(phone_number) for phone_number in already_used_phone_numbers]


if __name__ == "__main__":
    seeder = SystemPhone()
    seeder.create_system_phone()
