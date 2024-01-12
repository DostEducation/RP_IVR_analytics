import datetime
from faker import Faker
from api.models import ModuleContent as ModuleContentInstance
from api import db


class ModuleContent:
    faker = Faker()  # Kept for future use

    def create_module_content(self, module_id, content_id):
        module_instance = ModuleContentInstance()
        module_instance.module_id = module_id
        module_instance.content_id = content_id

        db.session.add(module_instance)
        db.session.commit()

        return module_instance


if __name__ == "__main__":
    seeder = ModuleContent()
    seeder.create_module_content(module_id=1, content_id=1)
