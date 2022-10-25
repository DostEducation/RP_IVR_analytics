from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class LanguageQuery(BaseQuery):
    def get_by_name(self, language):
        return self.filter_by(name=language).first()


class Language(TimestampMixin, db.Model):
    query_class = LanguageQuery
    __tablename__ = "language"

    class LanguageName(object):
        HINDI = "HINDI"
        ENGLISH = "ENGLISH"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
