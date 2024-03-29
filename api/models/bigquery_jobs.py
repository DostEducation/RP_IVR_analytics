from api import db


class BigqueryJobs(db.Model):
    __tablename__ = "bigquery_jobs"

    table_name = db.Column(db.String(100), primary_key=True, nullable=False)
    index = db.Column(db.String(100), server_default="0")
    bigquery_table_name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    last_updated_at = db.Column(
        db.DateTime,
        server_default="2000-01-01 00:00:00",
    )
