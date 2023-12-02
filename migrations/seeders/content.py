from faker import Faker
from random import randint
from api.models import Content as ContentModel
from api import db
from typing import List


class Content:
    faker = Faker()

    def get_random_duration(self):
        return randint(5, 100)

    def create_content(self) -> List:
        content_instances = []

        content_names = [
            "B-3_1-MODULE1_1-DAY1",
            "B-3_1-MODULE1_1-DAY2",
            "B-3_1-MODULE1_1-DAY3",
            "B-3_1-MODULE1_1-DAY4",
            "T-6_1-MODULE1_1-DAY1",
            "T-6_1-MODULE1_1-DAY2",
            "T-6_1-MODULE1_1-DAY3",
            "T-6_1-MODULE1_1-DAY4",
            "B-3_2-MODULE2_1-DAY1",
            "B-3_2-MODULE2_1-DAY2",
            "B-3_2-MODULE2_1-DAY3",
            "B-3_2-MODULE2_1-DAY4",
        ]

        for content_name in content_names:
            content = ContentModel()

            # Choose a random duration
            content_duration = self.get_random_duration()

            content.name = content_name
            content.status = "active"
            content.duration = content_duration

            content_instances.append(content)

        db.session.add_all(content_instances)
        db.session.commit()

        return content_instances


if __name__ == "__main__":
    seeder = Content()
    seeder.create_content()
