import logging, os
from api import app
from google.cloud import logging as cloud_logging

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

if os.getenv("FLASK_ENV") == "production":
    log_client = cloud_logging.Client()
    log_handler = log_client.get_default_handler()
    app.logger.addHandler(log_handler)
else:
    log_handler = logging.getLogger().handlers[0]
    app.logger.addHandler(log_handler)
