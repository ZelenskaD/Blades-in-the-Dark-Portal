from datetime import datetime

from schemas import db


class Campaign(db.Model):
    """Campaign model."""

    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    description = db.Column(db.String(2000), nullable=True)
    campaign_picture = db.Column(db.String(1000), default="/backgrounds/default-card.png")

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref='created_campaigns')

    characters = db.relationship('Character', backref='campaign_characters', lazy=True)
    sessions = db.relationship('Session', backref='campaign_sessions', lazy=True)
    crews = db.relationship('Crew', backref='campaign_crews', lazy=True)
    participants = db.relationship('UserCampaignParticipation', backref='campaign_participations', lazy=True)
    users = db.relationship('User', secondary='user_campaign_participations', back_populates='campaigns')

    def __init__(self, name, description, creator_id, campaign_picture=None):
        self.name = name
        self.description = description
        self.campaign_picture = campaign_picture or "/backgrounds/default-card.jpg"
        self.creator_id = creator_id

    def __repr__(self):
        return f'<Campaign {self.name}> , {self.description}, {self.campaign_picture}'

    @staticmethod
    def get_all():
        return Campaign.query.all()