from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery

class ModuleContentQuery(BaseQuery):

    def get_by_content_id(self, content_id):
        return self.filter(ModuleContent.content_id == content_id).first()

class ModuleContent(TimestampMixin, db.Model):
    query_class = ModuleContentQuery
    __tablename__ = 'module_content'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    is_optional = db.Column(db.Boolean)
