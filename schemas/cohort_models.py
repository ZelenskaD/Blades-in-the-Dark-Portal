from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from schemas import db


class Cohort(db.Model):
    """Cohort model."""

    __tablename__ = 'cohorts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    edges = db.Column(JSON, default=list)
    flaws = db.Column(JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    crew_id = db.Column(db.Integer, db.ForeignKey('crews.id'), nullable=False)

    crew = db.relationship('Crew', backref='cohort_crews')

    def __repr__(self):
        return f'<Cohort {self.type} {self.description} {self.edges} {self.flaws}>'

    @staticmethod
    def from_dict(data):
        return Cohort(
            type=data.get('type'),
            description=data.get('description'),
            edges=data.get('edges', []),
            flaws=data.get('flaws', []),
            crew_id=data.get('crew_id')
        )
