import datetime
from faker import Faker
from api.models import ProgramModule as ProgramModuleInstance
from api import db


class ProgramModule:
    faker = Faker()  # Kept for future use

    def create_program_module(self, program_id, module_id, sequence_id=1):
        program_module_instance = ProgramModuleInstance()
        program_module_instance.program_id = program_id
        program_module_instance.module_id = module_id
        program_module_instance.sequence = sequence_id

        db.session.add(program_module_instance)
        db.session.commit()

        return program_module_instance


if __name__ == "__main__":
    seeder = ProgramModule()
    seeder.create_program_module(program_id=1, module_id=1)
