import datetime
from faker import Faker
from api.models import Module as ModuleInstance
from api import db


class Module:
    faker = Faker()  # Kept for future use

    def create_module(self, program_id):
        module_instance = ModuleInstance()
        module_instance.name = "Test Module"
        module_instance.program_id = program_id

        db.session.add(module_instance)
        db.session.commit()

        return module_instance


if __name__ == "__main__":
    seeder = Module()
    seeder.create_module(program_id=1)
