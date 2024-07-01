from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.ext.mutable import MutableDict


class Trauma:
    def __init__(self, current: int = 0, maximum: int = 0):
        self.current = current
        self.maximum = maximum

    def to_dict(self):
        return {"current": self.current, "maximum": self.maximum}

    @classmethod
    def from_dict(cls, data):
        return cls(
            current=data.get("current", 0),
            maximum=data.get("maximum", 0)
        )

    def __repr__(self):
        return f"<Trauma(current={self.current}, maximum={self.maximum})>"


class TraumaType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        """
        Convert Attributes objects to dictionaries for storage in the database.
        """
        if value is not None and isinstance(value, Trauma):
            return value.to_dict()
        return value

    def process_result_value(self, value, dialect):
        """
        Convert dictionaries back to Attributes objects when retrieving from the database.
        """
        if value is not None:
            return Trauma.from_dict(value)
        return value


# Use MutableList to track changes in the JSON column
MutableDict.associate_with(TraumaType)
