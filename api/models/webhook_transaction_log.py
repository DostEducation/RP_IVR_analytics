from api.mixins import TimestampMixin
from api import db, helpers
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc, and_


class WebhookTransactionLogQuery(BaseQuery):
    def get_by_id(self, id):
        return self.filter(WebhookTransactionLog.id == id).first()


class WebhookTransactionLog(TimestampMixin, db.Model):
    query_class = WebhookTransactionLogQuery

    __tablename__ = "webhook_transaction_log"
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Text)
    processed = db.Column(db.Boolean, nullable=False)
    attempts = db.Column(db.Integer, nullable=False, default="0")
