from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.ext.mutable import MutableDict


class Prowess:
    def __init__(self, finnesse=0, prowl=0, skirmish=0, wreck=0):
        self.finnesse = finnesse
        self.prowl = prowl
        self.skirmish = skirmish
        self.wreck = wreck

    def to_dict(self):
        return {"finnesse": self.finnesse, "prowl": self.prowl, "skirmish": self.skirmish, "wreck": self.wreck}

    @classmethod
    def from_dict(cls, data):
        return cls(
            finnesse=data.get("finnesse", 0),
            prowl=data.get("prowl", 0),
            skirmish=data.get("skirmish", 0),
            wreck=data.get("wreck", 0)
        )

    def __repr__(self):
        return f"<Prowess(finnesse={self.finnesse}, prowl={self.prowl}, skirmish={self.skirmish}, wreck={self.wreck})>"


# Attributes Type is a custom SQLAlchemy TypeDecorator for handling lists of Attributes objects stored as JSON.
class ProwessType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        """
        Convert Attributes objects to dictionaries for storage in the database.
        """
        if value is not None and isinstance(value, Prowess):
            return value.to_dict()
        return value

    def process_result_value(self, value, dialect):
        """
        Convert dictionaries back to Attributes objects when retrieving from the database.
        """
        if value is not None:
            return Prowess.from_dict(value)
        return value


# Use MutableList to track changes in the JSON column
MutableDict.associate_with(ProwessType)
