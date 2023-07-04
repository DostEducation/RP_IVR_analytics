from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class ContentQuery(BaseQuery):
    def get_by_id(self, content_id):
        return self.filter(Content.id == content_id).first()


class Content(TimestampMixin, db.Model):
    query_class = ContentQuery
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    type = db.Column(db.String(100))
