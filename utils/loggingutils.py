import logging
from api import app
from google.cloud import logging as gcloud_logging

logging.basicConfig(level=logging.DEBUG)

if app.config["FLASK_ENV"] == "development":
    logger = logging.getLogger()
    log_handler = logger.handlers[0]
    logger.addHandler(log_handler)
else:
    log_client = gcloud_logging.Client()
    log_client.setup_logging()
    log_handler = log_client.get_default_handler()
    logger = app.logger
    logger.addHandler(log_handler)
