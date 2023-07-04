# This file is treated as service layer
from api import models, helpers, app
import json
from utils.loggingutils import logger


class TransactionLogService:
    def create_new_webhook_log(self, jsonData):
        try:
            new_webhook_log = models.WebhookTransactionLog(
                payload=json.dumps(jsonData), processed=False
            )
            helpers.save(new_webhook_log)
            return new_webhook_log
        except Exception as e:
            logger.error(
                f"Error while creating new webhook log. Webhook: {jsonData}. Error message: {e}"
            )
            return None

    def mark_webhook_log_as_processed(self, webhook_log):
        try:
            webhook_log.processed = True
            helpers.save(webhook_log)
        except Exception as e:
            logger.error(
                f"Error while marking webhook log as processed. Error message: {e}"
            )

    def get_failed_webhook_transaction_log(self):
        try:
            failed_webhook_transaction_logs = (
                models.WebhookTransactionLog.query.filter(
                    models.WebhookTransactionLog.processed.is_(False)
                )
                .filter(
                    models.WebhookTransactionLog.attempts
                    < app.config["MAX_RETRY_ATTEMPTS_FOR_LOGS"]
                )
                .order_by(models.WebhookTransactionLog.created_on)
                .limit(app.config["RETRY_LOGS_BATCH_LIMIT"])
                .all()
            )

            return failed_webhook_transaction_logs
        except Exception as e:
            logger.error(
                f"Error while retrieving failed webhook transaction logs. Error message: {e}"
            )
            return None
