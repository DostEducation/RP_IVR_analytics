from api.mixins import TimestampMixin
from api import db


class IvrCallbackTransactionLog(TimestampMixin, db.Model):
    __tablename__ = "ivr_callback_transaction_log"

    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Text)
    processed = db.Column(db.Boolean, nullable=False)
    attempts = db.Column(db.Integer, nullable=False, default="0")
