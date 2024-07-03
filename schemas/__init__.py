
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

from .campaign_models import Campaign
from schemas.character_models import Character
from .session_models import Session
from .user_campaign_participation_models import UserCampaignParticipation
from .user_models import User


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
    bcrypt.init_app(app)
    # db.drop_all()
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"An error occurred: {e}")
