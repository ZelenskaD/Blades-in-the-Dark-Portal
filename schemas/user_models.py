from schemas import db, bcrypt
from schemas.user_campaign_participation_models import UserCampaignParticipation


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    campaigns = db.relationship('Campaign', secondary='user_campaign_participations', back_populates='users')
    characters = db.relationship('Character', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password_hash=hashed_pwd,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`."""
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return False

    @staticmethod
    def get_all():
        return User.query.all()
