import logging, os
from api import app
from google.cloud import logging as gcloud_logging

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

if os.getenv("FLASK_ENV") == "development":
    log_handler = logging.getLogger().handlers[0]
    app.logger.addHandler(log_handler)
else:
    log_client = gcloud_logging.Client()
    log_client.setup_logging()
    log_handler = log_client.get_default_handler()
    app.logger.addHandler(log_handler)
