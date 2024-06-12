# from datetime import datetime
#
# from schemas import db
#
#
# class Campaign(db.Model):
#     """Campaign model."""
#
#     __tablename__ = 'campaigns'
#
#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )
#
#     name = db.Column(db.String(128), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
#
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#
#     def __repr__(self):
#         return f'<Campaign {self.name}>'
#
#     @staticmethod
#     def get_all():
#         return Campaign.query.all()