from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class UserModuleContentQuery(BaseQuery):
    def get_user_module_content(
        self, user_program_id, program_module_id, module_content_id
    ):
        return self.filter(
            UserModuleContent.user_program_id == user_program_id,
            UserModuleContent.program_module_id == program_module_id,
            UserModuleContent.module_content_id == module_content_id,
        ).first()


class UserModuleContent(TimestampMixin, db.Model):
    query_class = UserModuleContentQuery
    __tablename__ = "user_module_content"
    id = db.Column(db.Integer, primary_key=True)
    user_program_id = db.Column(db.Integer, db.ForeignKey("user_program.id"))
    program_module_id = db.Column(db.Integer, db.ForeignKey("program_module.id"))
    module_content_id = db.Column(db.Integer, db.ForeignKey("module_content.id"))
    status = db.Column(db.String(50))
