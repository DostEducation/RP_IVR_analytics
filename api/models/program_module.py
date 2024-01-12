from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy.query import Query as BaseQuery


class ProgramModuleQuery(BaseQuery):
    def get_by_module_id(self, module_id):
        return self.filter(ProgramModule.module_id == module_id).first()


class ProgramModule(TimestampMixin, db.Model):
    query_class = ProgramModuleQuery
    __tablename__ = "program_module"
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    sequence = db.Column(db.Integer)
