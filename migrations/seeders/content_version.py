from faker import Faker
from api.models import ContentVersion as ContentVersionModel, Content as ContentModel
from typing import List
from api import db


class ContentVersion:
    faker = Faker()  # Kept for future use

    def create_content_version(self, language_id: int, contents: List[ContentModel]):
        content_version_instances = []

        for content in contents:
            content_version = ContentVersionModel()
            content_version.content_id = content.id
            content_version.duration = content.duration
            content_version.language_id = language_id
            content_version.status = "active"

            content_version_instances.append(content_version)

        db.session.add_all(content_version_instances)
        db.session.commit()


if __name__ == "__main__":
    seeder = ContentVersion()
    seeder.create_content_version(language_id=1, contents=[])
