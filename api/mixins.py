from __future__ import absolute_import

from api import db

class TimestampMixin(object):
    created_on = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    updated_on = db.Column(
        db.DateTime,
        server_onupdate=db.func.now(),
        server_default=db.func.now()
    )