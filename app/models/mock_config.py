from app.main import db 
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class MockConfig(db.Model):
    __tablename__ = "mock_configs"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    query_params = db.Column(JSON, default={})
    body_params = db.Column(JSON, default={})
    headers = db.Column(JSON, default={})
    response_status = db.Column(db.Integer, default=200)
    response_body = db.Column(JSON, default={})
    content_type = db.Column(db.String(100), default="application/json")
    delay_ms = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<MockConfig {self.method} {self.path}>"
