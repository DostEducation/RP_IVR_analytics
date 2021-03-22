from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery

class IvrPromptResponseQuery(BaseQuery):

    def get_by_call_log_id(self, call_log_id):
        return self.filter(IvrPromptResponse.call_log_id == call_log_id).all()

class IvrPromptResponse(TimestampMixin, db.Model):
    query_class = IvrPromptResponseQuery
    __tablename__ = 'ivr_prompt_response'
    id = db.Column(db.Integer, primary_key=True)
    prompt_name = db.Column(db.String(255), nullable=False)
    prompt_question = db.Column(db.String(500))
    response = db.Column(db.String(255))
    user_phone = db.Column(db.String(50))
    is_call_log_processed = db.Column(db.Boolean)
    call_sid = db.Column(db.Integer)
    call_log_id = db.Column(db.Integer, db.ForeignKey('call_log.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    keypress = db.Column(db.Integer)
