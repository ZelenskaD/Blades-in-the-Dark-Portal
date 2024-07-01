from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.ext.mutable import MutableList

class Ability:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_dict(self):
        return {"name": self.name, "description": self.description}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], description=data["description"])

    def __repr__(self):
        return f"<Ability(name={self.name}, description={self.description})>"

class AbilitiesType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        if value is not None:
            return [ability.to_dict() for ability in value if isinstance(ability, Ability)]
        return []

    def process_result_value(self, value, dialect):
        if value is not None:
            return [Ability.from_dict(ability) for ability in value]
        return []

MutableList.associate_with(AbilitiesType)

