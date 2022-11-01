from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class IvrPromptMappingQuery(BaseQuery):
    def get_by_ivr_prompt_id(self, ivr_prompt_id):
        return self.filter(IvrPromptMapping.ivr_prompt_id == ivr_prompt_id).all()


class IvrPromptMapping(TimestampMixin, db.Model):
    query_class = IvrPromptMappingQuery
    __tablename__ = "ivr_prompt_mapping"
    id = db.Column(db.Integer, primary_key=True)
    ivr_prompt_id = db.Column(db.Integer, db.ForeignKey("ivr_prompt.id"))
    mapped_table_name = db.Column(db.String(255))
    mapped_table_column_name = db.Column(db.String(255))
    default_value = None
