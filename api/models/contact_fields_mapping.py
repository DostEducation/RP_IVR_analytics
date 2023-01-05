from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class ContactFieldsMappingQuery(BaseQuery):
    def get_by_field_name(self, custom_fields):
        try:
            return self.filter(ContactFieldsMapping.field_name == custom_fields).all()
        except Exception as e:
            print(f"Exception occurred: {e}")

    def get_by_group_name(self, contact_groups):
        try:
            return self.filter(ContactFieldsMapping.field_name == contact_groups).all()
        except Exception as e:
            print(f"Exception occurred: {e}")


class ContactFieldsMapping(db.Model):
    query_class = ContactFieldsMappingQuery
    __tablename__ = "contact_fields_mapping"
    id = db.Column(db.Integer, primary_key=True)
    field_type = db.Column(db.String(255))
    field_name = db.Column(db.String(255))
    mapped_table_name = db.Column(db.String(255))
    mapped_table_column_name = db.Column(db.String(255))
    mapped_table_column_value = db.Column(db.String(255))
    expected_field_data_type = db.Column(db.String(255), nullable=True)
    expected_field_value = db.Column(db.String(255), nullable=True)
