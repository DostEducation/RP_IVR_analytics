from api.mixins import TimestampMixin
from api import db

class UserModuleContent(TimestampMixin, db.Model):
    __tablename__ = 'user_module_content'
    id = db.Column(db.Integer, primary_key=True)
    user_program_id = db.Column(db.Integer, db.ForeignKey('user_program.id'))
    program_module_id = db.Column(db.Integer, db.ForeignKey('program_module.id'))
    module_content_id = db.Column(db.Integer, db.ForeignKey('module_content.id'))
    status = db.Column(db.String(50))
