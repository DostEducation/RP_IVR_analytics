from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class ProgramSequenceQuery(BaseQuery):
    def get_by_module_content_program_ids(self, program_id, module_id, content_id):
        return self.filter_by(
            content_id=content_id,
            program_id=program_id,
            module_id=module_id,
        ).first()


class ProgramSequence(TimestampMixin, db.Model):
    query_class = ProgramSequenceQuery
    __tablename__ = "program_sequence"

    class ContentStatus(object):
        ACTIVE = "active"
        INACTIVE = "inactive"

    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
