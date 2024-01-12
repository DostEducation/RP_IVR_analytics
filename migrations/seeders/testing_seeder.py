from faker import Faker
from typing import List
from migrations.seeders.user import User
from migrations.seeders.system_phone import SystemPhone
from migrations.seeders.partner import Partner
from migrations.seeders.registration import Registration
from migrations.seeders.program import Program
from migrations.seeders.language import Language
from migrations.seeders.content_version import ContentVersion
from migrations.seeders.content import Content
from migrations.seeders.user_program import UserProgram
from migrations.seeders.module import Module
from migrations.seeders.module_content import ModuleContent
from migrations.seeders.program_module import ProgramModule
from migrations.seeders.program_sequence import ProgramSequence


def main():
    # Running seeders sequentially

    language = Language()
    language_instance = language.create_language(name="ENGLISH")

    content = Content()
    created_contents = content.create_content()

    content_version = ContentVersion()
    content_version.create_content_version(
        language_id=language_instance.id, contents=created_contents
    )

    partner = Partner()
    partner_instance = partner.create_partner(name="UNICEF", email="unicef@test.com")

    user = User()
    created_user_instances = user.create_user(partner_id=partner_instance.id)

    system_phone = SystemPhone()
    system_phone_numbers = system_phone.create_system_phone()

    registration = Registration()
    registration.create_registration(
        user_id=created_user_instances[0].user_id,
        user_phone_number=created_user_instances[0].phone,
        system_phone_number=system_phone_numbers[0],
        partner_id=partner_instance.id,
    )

    program = Program()
    created_programs: List = program.create_programs()

    user_program = UserProgram()
    created_user_programs: List = user_program.create_user_program(
        created_programs, [user.user_id for user in created_user_instances]
    )

    module = Module()
    created_module = module.create_module(program_id=created_programs[0].id)

    module_content = ModuleContent()
    created_module_content = module_content.create_module_content(
        module_id=created_module.id, content_id=created_contents[0].id
    )

    program_module = ProgramModule()
    create_program_module = program_module.create_program_module(
        program_id=created_programs[0].id, module_id=created_module.id
    )

    program_sequence = ProgramSequence()
    created_program_sequence = program_sequence.create_program_sequence(
        program_id=created_programs[0].id,
        content_id=created_contents[0].id,
        module_id=created_module.id,
    )
