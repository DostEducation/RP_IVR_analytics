import logging
from api import app
from google.cloud import logging as gcloud_logging

logger = app.logger
logging.basicConfig(level=logging.DEBUG)

if app.config["FLASK_ENV"] == "development":
    log_handler = logging.getLogger().handlers[0]
    logger.addHandler(log_handler)
else:
    log_client = gcloud_logging.Client()
    log_client.setup_logging()
    log_handler = log_client.get_default_handler()
    logger.addHandler(log_handler)
