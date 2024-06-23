from sqlalchemy.dialects.postgresql import JSON
from schemas import db


class Character(db.Model):
    """Character model."""

    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    alias = db.Column(db.String(100), nullable=False)
    look = db.Column(JSON, default=list)
    heritage = db.Column(db.String(600), nullable=False)
    background = db.Column(db.String(600), nullable=False)
    vice = db.Column(db.String(600), nullable=False)
    stress = db.Column(JSON, default=list)
    trauma = db.Column(JSON, default=list)
    abilities = db.Column(JSON, default=list)
    friend = db.Column(JSON, default=list)
    enemy = db.Column(JSON, default=list)
    allitems = db.Column(JSON, default=list)
    equippeditems = db.Column(JSON, default=list)
    attributes = db.Column(JSON, default=list)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=True)

    user = db.relationship('User', backref='user_characters')
    campaign = db.relationship('Campaign', backref='campaign_characters')

    def __repr__(self):
        return (f'<Character {self.name} {self.alias} {self.look} {self.heritage} {self.background} {self.vice} '
                f'{self.stress} {self.trauma} {self.abilities} {self.equippeditems} {self.attributes} {self.user_id} '
                f'{self.campaign_id}>')
