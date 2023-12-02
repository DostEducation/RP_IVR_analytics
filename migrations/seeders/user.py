import datetime
from faker import Faker
from random import randint
from api.models import User as UserModel
from api import db
from uuid import uuid4


class CreatedUserInstance:
    def __init__(self, user_instance: UserModel) -> None:
        self.user_id = user_instance.id
        self.phone = user_instance.phone
        self.partner_id = user_instance.partner_id


class User:
    faker = Faker()

    def generate_random_phone_numbers(self):
        return randint(10000000, 99999999)

    def create_user(self, count=10, partner_id=1):
        already_used_phone_numbers = set({})
        user_instances = []

        for _ in range(count):
            search_new_phone_number = True
            current_phone_number = None
            while search_new_phone_number:
                new_phone_number = self.generate_random_phone_numbers()
                if not new_phone_number in already_used_phone_numbers:
                    current_phone_number = new_phone_number
                    already_used_phone_numbers.add(new_phone_number)
                    search_new_phone_number = False

            user_instance = UserModel()
            user_instance.phone = f"+91{current_phone_number}"
            user_instance.partner_id = partner_id
            user_instance.name = str(uuid4())[:16]

            user_instances.append(user_instance)

        db.session.add_all(user_instances)
        db.session.commit()

        return [CreatedUserInstance(user) for user in user_instances]


if __name__ == "__main__":
    seeder = User()
    seeder.create_user()
