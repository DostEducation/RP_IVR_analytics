from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy.query import Query as BaseQuery


class ContentVersionQuery(BaseQuery):
    def get_by_id(self, content_version_id):
        return self.filter(ContentVersion.id == content_version_id).first()

    def get_by_language_and_content_id(self, language_id, content_id):
        return self.filter(
            ContentVersion.content_id == content_id,
            ContentVersion.language_id == language_id,
            ContentVersion.status == "active",
        ).first()


class ContentVersion(TimestampMixin, db.Model):
    query_class = ContentVersionQuery
    __tablename__ = "content_version"

    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id", ondelete="cascade"))
    language_id = db.Column(
        db.Integer, db.ForeignKey("language.id", ondelete="cascade")
    )
    version = db.Column(db.Float)
    duration = db.Column(db.Integer)
    status = db.Column(db.String(50))
