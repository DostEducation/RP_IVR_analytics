from api.mixins import TimestampMixin
from api import db

class ModuleContent(TimestampMixin, db.Model):
    __tablename__ = 'module_content'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    sequence = db.Column(db.Integer)
    is_optional = db.Column(db.Boolean)
