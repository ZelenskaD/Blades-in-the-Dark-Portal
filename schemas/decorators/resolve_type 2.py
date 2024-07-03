from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.ext.mutable import MutableDict


class Resolve:
    def __init__(self, attune=0, command=0, consort=0, sway=0):
        self.attune = attune
        self.command = command
        self.consort = consort
        self.sway = sway

    def to_dict(self):
        return {"attune": self.attune, "command": self.command, "consort": self.consort, "sway": self.sway}

    @classmethod
    def from_dict(cls, data):
        return cls(
            attune=data.get("attune", 0),
            command=data.get("command", 0),
            consort=data.get("consort", 0),
            sway=data.get("sway", 0)
        )

    def __repr__(self):
        return f"<Resolve(attune={self.attune},  command={self.command}, consort={self.consort}, sway={self.sway})>"


# Attributes Type is a custom SQLAlchemy TypeDecorator for handling lists of Attributes objects stored as JSON.

class ResolveType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        """
        Convert Attributes objects to dictionaries for storage in the database.
        """
        if value is not None and isinstance(value, Resolve):
            return value.to_dict()
        return value

    def process_result_value(self, value, dialect):
        """
        Convert dictionaries back to Attributes objects when retrieving from the database.
        """
        if value is not None:
            return Resolve.from_dict(value)
        return value


# Use MutableList to track changes in the JSON column
MutableDict.associate_with(ResolveType)