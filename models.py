from app import db
from datetime import datetime

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    cpu_specs = db.Column(db.String(100), nullable=False)
    ram_gb = db.Column(db.Integer, nullable=False)
    storage_gb = db.Column(db.Integer, nullable=False)
    os_version = db.Column(db.String(50), nullable=False)
    last_maintenance = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Machine {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='technician')
    last_login = db.Column(db.DateTime)