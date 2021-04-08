from api.mixins import TimestampMixin
from api import db


class IvrPromptMapping(TimestampMixin, db.Model):
    __tablename__ = "ivr_prompt_mapping"
    id = db.Column(db.Integer, primary_key=True)
    ivr_prompt_id = db.Column(db.Integer, db.ForeignKey("ivr_prompt.id"))
    mapped_table_name = db.Column(db.String(255))
    mapped_table_column_name = db.Column(db.String(255))
