from datetime import datetime
from flask_login import UserMixin
from backend.extensions import db   # ✅ correct import — no circular import

# ✅ Remove "db = db" → not needed at all


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role     = db.Column(db.String(20), default='user')

    # Relationship
    documents = db.relationship('Document', backref='uploader', lazy=True)


class Document(db.Model):
    __tablename__ = "document"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    filename    = db.Column(db.String(200), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags        = db.Column(db.String(200))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    version     = db.Column(db.Integer, default=1)


class Audit(db.Model):
    __tablename__ = "audit"

    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action    = db.Column(db.String(50), nullable=False)
    filename  = db.Column(db.String(200), nullable=False)
    version   = db.Column(db.Integer, nullable=False, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user      = db.relationship('User')
