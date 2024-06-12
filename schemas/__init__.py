from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
    bcrypt.init_app(app)
    db.drop_all()
    db.create_all()
