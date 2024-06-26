
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

from .campaign_models import Campaign
from .character_models import Character
from .cohort_models import Cohort
from .crew_models import Crew
from .session_models import Session
from .user_campaign_participation_models import UserCampaignParticipation
from .user_models import User


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
    bcrypt.init_app(app)
    # db.drop_all()
    db.create_all()
