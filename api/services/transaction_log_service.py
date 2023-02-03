# This file is treated as service layer
from api import models, helpers, app
import json, logging

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TransactionLogService(object):
    def create_new_webhook_log(self, jsonData):
        try:
            new_webhook_log = models.WebhookTransactionLog(
                payload=json.dumps(jsonData), processed=False
            )
            helpers.save(new_webhook_log)
            logger.info("New webhook log created successfully.")
            return new_webhook_log
        except Exception as e:
            logger.error("Error while creating new webhook log: %s" % e)

    def mark_webhook_log_as_processed(self, webhook_log):
        try:
            webhook_log.processed = True
            helpers.save(webhook_log)
            logger.info("Webhook log marked as processed successfully.")
        except Exception as e:
            logger.error("Error while marking webhook log as processed: %s" % e)

    def get_failed_webhook_transaction_log(self):
        try:
            failed_webhook_transaction_logs = (
                models.WebhookTransactionLog.query.filter(
                    models.WebhookTransactionLog.processed == False
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
                "Error while retrieving failed webhook transaction logs: %s" % e
            )
