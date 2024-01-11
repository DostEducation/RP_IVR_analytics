from api import db
from flask_sqlalchemy.query import Query as BaseQuery
from utils.loggingutils import logger


class ContactFieldsMappingQuery(BaseQuery):
    def get_by_field_name(self, field_name, field_value):
        try:
            return self.filter(
                ContactFieldsMapping.field_name == field_name,
                ContactFieldsMapping.expected_field_value == field_value,
            ).all()
        except Exception as e:
            logger.error(
                f"Exception occurred while fetching contact field mapping using"
                f"field name: {field_name} and value: {field_value}. Error message: {e}"
            )
            return None

    def get_by_group_name(self, contact_groups):
        try:
            return self.filter(ContactFieldsMapping.field_name == contact_groups).all()
        except Exception as e:
            logger.error(
                f"Exception occurred while fetching contact field mapping using group name {contact_groups}."
                f"Erorr message: {e}"
            )
            return None

    def get_all_contact_fields_mapping(self):
        try:
            return self.all()
        except Exception as e:
            logger.error(
                f"Exception occurred while getting all contact fiels mappings: {e}"
            )
            return None


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
