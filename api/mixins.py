from __future__ import absolute_import

from api import db
from datetime import datetime


class TimestampMixin:
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
