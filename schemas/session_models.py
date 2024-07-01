from datetime import datetime
from schemas import db


class Session(db.Model):
    """Session model."""

    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    notes = db.Column(db.String(200000), nullable=True)

    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False)
    campaign = db.relationship('Campaign', backref='session_campaigns')

    def __repr__(self):
        return f'<Session {self.title}>'

