import datetime
from faker import Faker
from api.models import ProgramSequence as ProgramSequenceInstance
from api import db


class ProgramSequence:
    faker = Faker()  # Kept for future use

    def create_program_sequence(self, content_id, program_id, module_id):
        program_sequence_instance = ProgramSequenceInstance()
        program_sequence_instance.program_id = program_id
        program_sequence_instance.content_id = content_id
        program_sequence_instance.module_id = module_id

        db.session.add(program_sequence_instance)
        db.session.commit()

        return program_sequence_instance


if __name__ == "__main__":
    seeder = ProgramSequence()
    seeder.create_program_sequence(program_id=1, content_id=1, module_id=1)
