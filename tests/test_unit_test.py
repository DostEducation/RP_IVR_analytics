from __future__ import absolute_import
from faker import Faker

faker = Faker()


def test_unit_test(app, db, setup_test_environment):
    assert 1 + 1 == 2
