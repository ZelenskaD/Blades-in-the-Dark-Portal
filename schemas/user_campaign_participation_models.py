from schemas import db


class UserCampaignParticipation(db.Model):

    __tablename__ = 'user_campaign_participations'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False, primary_key=True)

    user = db.relationship('User', backref='participations')
    campaign = db.relationship('Campaign', backref='user_participations')

