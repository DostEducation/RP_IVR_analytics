import datetime
from faker import Faker
from api.models import Program as ProgramModel
from api import db
from typing import List


class Program:
    faker = Faker()  # Kept for future use

    def create_programs(self) -> List:
        program_start_date = "2021-02-23"
        programs = [
            {"name": "B-3", "description": "Birth to Three", "program_type": "regular"},
            {"name": "T-6", "description": "Three to Six", "program_type": "regular"},
            {"name": "Intro", "description": "Intro", "program_type": "intro"},
        ]

        program_instances = []

        for program in programs:
            program_instance = ProgramModel()
            program_instance.name = program["name"]
            program_instance.description = program["description"]
            program_instance.program_type = program["program_type"]
            program_instance.start_date = program_start_date
            program_instance.created_on = datetime.datetime.now()
            program_instance.updated_on = datetime.datetime.now()

            program_instances.append(program_instance)

        db.session.add_all(program_instances)
        db.session.commit()

        return program_instances


if __name__ == "__main__":
    seeder = Program()
    seeder.create_program()
