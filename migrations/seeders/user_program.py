from random import randint
from faker import Faker
from api.models import UserProgram as UserProgramModel
from api import db
from typing import List


class UserProgram:
    faker = Faker()  # Kept for future use

    def randomly_select_preferred_timing_slot(self):
        slot_names = ["EVENING", "AFTERNOON", "MORNING"]
        return randint(0, len(slot_names) - 1)

    def randomly_select_a_program(self, programs: List) -> UserProgramModel:
        return programs[randint(0, len(programs) - 1)]

    def create_user_program(self, programs: List, user_ids: List) -> List:
        user_program_instances = []

        for user_id in user_ids:
            user_program = UserProgramModel()

            # Randomly select a program
            program: UserProgramModel = self.randomly_select_a_program(programs)

            # Randomly select preferred slot
            preferred_slot = self.randomly_select_preferred_timing_slot()

            user_program.user_id = user_id
            user_program.preferred_time_slot = preferred_slot
            user_program.program_id = program.id

            user_program_instances.append(user_program)

        db.session.add_all(user_program_instances)
        db.session.commit()

        return user_program_instances


if __name__ == "__main__":
    seeder = UserProgram()
    seeder.create_user_program()
