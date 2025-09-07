# ---------- SQLAlchemy Models ----------
from datetime import datetime
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def cycle_status(self):
        order = ["Pending", "In Progress", "Done"]
        try:
            idx = order.index(self.status)
        except ValueError:
            idx = 0
        self.status = order[(idx + 1) % len(order)]
        return self.status
