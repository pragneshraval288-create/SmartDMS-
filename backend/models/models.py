from datetime import datetime
from flask_login import UserMixin
from backend.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    # ✅ Login + Basic Profile
    username = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    mobile = db.Column(db.String(20), unique=True, nullable=True)
    dob = db.Column(db.String(20), nullable=True)

    # ✅ Profile Picture
    profile_pic = db.Column(
        db.String(200),
        default="default_user.png",
        nullable=True
    )

    # ✅ Auth
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Relationship
    documents = db.relationship("Document", backref="uploader", lazy=True)


class Document(db.Model):
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    filename = db.Column(db.String(200))
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tags = db.Column(db.String(200))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.Integer, default=1)


class Audit(db.Model):
    __tablename__ = "audit"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    action = db.Column(db.String(50))
    filename = db.Column(db.String(200))
    version = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")
