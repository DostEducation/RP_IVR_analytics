# This file is treated as service layer
from api import models, helpers, app
import json


class TransactionLogService(object):
    def create_new_webhook_log(self, jsonData):
        new_webhook_log = models.WebhookTransactionLog(
            payload=json.dumps(jsonData), processed=False
        )
        helpers.save(new_webhook_log)
        return new_webhook_log

    def mark_webhook_log_as_processed(self, webhook_log):
        webhook_log.processed = True
        helpers.save(webhook_log)

    def get_failed_webhook_transaction_log(self):
        failed_webhook_transaction_logs = (
            models.WebhookTransactionLog.query.filter(
                models.WebhookTransactionLog.processed == False
            )
            .filter(
                models.WebhookTransactionLog.attempts
                <= app.config["MAX_RETRY_ATTEMPTS_FOR_LOGS"]
            )
            .order_by(models.WebhookTransactionLog.created_on)
            .limit(app.config["RETRY_LOGS_BATCH_LIMIT"])
            .all()
        )

        return failed_webhook_transaction_logs
