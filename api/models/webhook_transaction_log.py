from api.mixins import TimestampMixin
from api import db
from flask_sqlalchemy import BaseQuery


class WebhookTransactionLogQuery(BaseQuery):
    def get_by_id(self, webhook_transaction_log_id):
        return self.filter(
            WebhookTransactionLog.id == webhook_transaction_log_id
        ).first()

    def get_last_record(self):
        return self.filter().order_by(WebhookTransactionLog.id.desc()).first()


class WebhookTransactionLog(TimestampMixin, db.Model):
    query_class = WebhookTransactionLogQuery

    __tablename__ = "webhook_transaction_log"
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Text)
    processed = db.Column(db.Boolean, nullable=False)
    attempts = db.Column(db.Integer, nullable=False, default="0")
