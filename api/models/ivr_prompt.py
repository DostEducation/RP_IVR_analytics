from api.mixins import TimestampMixin
from api import db, models
from sqlalchemy import desc, and_
from flask_sqlalchemy import BaseQuery


class IvrPromptQuery(BaseQuery):
    def get_by_name(self, name, response):
        return (
            self.filter(
                and_(
                    IvrPrompt.prompt_name == name,
                    IvrPrompt.possible_response == response,
                    IvrPrompt.status == models.IvrPrompt.IvrStatus.ACTIVE,
                )
            )
            .order_by(desc(IvrPrompt.created_on))
            .first()
        )


class IvrPrompt(TimestampMixin, db.Model):
    query_class = IvrPromptQuery
    __tablename__ = "ivr_prompt"

    class IvrStatus(object):
        ACTIVE = "active"
        INACTIVE = "inactive"

    id = db.Column(db.Integer, primary_key=True)
    prompt_name = db.Column(db.String(255), nullable=False)
    prompt_question = db.Column(db.String(500))
    possible_response = db.Column(db.String(255))
    status = db.Column(db.String(50))
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))
    keypress = db.Column(db.Integer)
