from faker import Faker
from api.models import Language as LanguageModel
from api import db


class Language:
    faker = Faker()  # Kept for future use

    def create_language(self, name) -> LanguageModel:
        language_record = LanguageModel()
        language_record.name = name

        db.session.add(language_record)
        db.session.commit()

        return language_record


if __name__ == "__main__":
    seeder = Language()
    seeder.create_language(name="ENGLISH")
