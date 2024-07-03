from schemas import db
from schemas.decorators.abilities_type import AbilitiesType
from schemas.decorators.contact_type import Contact
# from schemas.decorators.experience_type import ExperienceType, Experience
from schemas.decorators.insight_type import InsightType, Insight
from schemas.decorators.prowess_type import ProwessType, Prowess
from schemas.decorators.resolve_type import ResolveType, Resolve
from schemas.decorators.stress_type import StressType, Stress
from schemas.decorators.trauma_type import TraumaType, Trauma
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class Character(db.Model):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)

    name = Column(String(30), nullable=False)
    alias = Column(String(100), nullable=False)
    look = Column(String(2000), nullable=True)
    image_url = Column(String(2000), nullable=True)  # Add this line

    image = Column(String(2000), nullable=True)

    heritage = Column(String(600), nullable=False)
    background = Column(String(600), nullable=False)
    vice = Column(String(600), nullable=False)
    experience = Column(Integer, nullable=False, default=0)

    # experience = Column(MutableDict.as_mutable(JSON))
    stress = Column(MutableDict.as_mutable(JSON), nullable=False, default=lambda: Stress().to_dict())
    trauma = Column(MutableDict.as_mutable(JSON), nullable=False, default=lambda: Trauma().to_dict())

    abilities = Column(MutableList.as_mutable(AbilitiesType), nullable=False, default=list)

    friend = Column(MutableDict.as_mutable(JSON), nullable=False, default=lambda: Contact().to_dict())
    enemy = Column(MutableDict.as_mutable(JSON), nullable=False, default=lambda: Contact().to_dict())

    insight = Column(MutableDict.as_mutable(JSON), nullable=False, default=lambda: Insight().to_dict())
    prowess = Column(MutableDict.as_mutable(JSON), nullable=False, default=lambda: Prowess().to_dict())
    resolve = Column(MutableDict.as_mutable(JSON), nullable=False, default=lambda: Resolve().to_dict())
    playbook_name = Column(db.String(64), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=True)

    user = db.relationship('User', backref='user_characters')
    campaign = db.relationship('Campaign', backref='campaign_characters')

    def __repr__(self):
        return (f'<Character {self.name} {self.alias} {self.look} {self.heritage} {self.background} {self.vice} '
                f'{self.stress} {self.trauma} {self.abilities} {self.friend} {self.enemy} '
                f'{self.insight} {self.prowess} {self.resolve} {self.user_id} {self.campaign_id}>')
