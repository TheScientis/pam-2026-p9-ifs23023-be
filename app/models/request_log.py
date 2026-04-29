from app.extensions import db
from datetime import datetime, timezone

class RequestLog(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
