from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.ext.mutable import MutableDict


class Contact:
    def __init__(self, name: str = "", occupation: str = ""):
        self.name = name
        self.occupation = occupation

    def to_dict(self):
        return {"name": self.name, "occupation": self.occupation}

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            occupation=data.get("occupation", "")
        )

    def __repr__(self):
        return f"<Contact(name={self.name}, occupation={self.occupation})>"








