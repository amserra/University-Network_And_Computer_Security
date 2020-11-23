"""Data models."""
from . import db

class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(64),
        nullable=False
    )
    email = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        nullable=False
    )
    email_verified = db.Column(
        db.Boolean,
        index=False,
        default=0,
        nullable=False
    )

    def __repr__(self):
        return "<User {}>".format(self.username)