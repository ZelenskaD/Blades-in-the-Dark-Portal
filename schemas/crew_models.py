from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from schemas import db


class Crew(db.Model):
    """Crew model."""

    __tablename__ = 'crews'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    reputation = db.Column(db.String(100), nullable=False)
    abilities = db.Column(JSON, default=list)
    contacts = db.Column(JSON, default=list)
    upgrades = db.Column(JSON, default=list)
    attributes = db.Column(JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # cohorts = db.relationship('Cohort', back_populates='crew', cascade='all, delete-orphan')

    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    campaign = db.relationship('Campaign', backref='crew_campaigns')

    def __repr__(self):
        return f'<Crew {self.name} {self.reputation} {self.abilities} {self.contacts}> {self.upgrades} {self.attributes} {self.created_at} {self.updated_at}>'

    @staticmethod
    def from_dict(data):
        """Create a Crew instance from a dictionary."""
        return Crew(
            name=data.get('name'),
            reputation=data.get('reputation'),
            abilities=data.get('abilities', []),
            contacts=data.get('contacts', []),
            upgrades=data.get('upgrades', []),
            attributes=data.get('attributes', [])
        )
