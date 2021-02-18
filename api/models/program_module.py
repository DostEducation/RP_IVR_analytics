from api.mixins import TimestampMixin
from api import db

class ProgramModule(TimestampMixin, db.Model):
    __tablename__ = 'program_module'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    sequence = db.Column(db.Integer)
