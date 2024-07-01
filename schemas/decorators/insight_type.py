from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.ext.mutable import MutableDict


class Insight:
    def __init__(self, hunt: int = 0, study: int = 0, survey: int = 0, tinker: int = 0):
        self.hunt = hunt
        self.study = study
        self.survey = survey
        self.tinker = tinker

    def to_dict(self):
        return {"hunt": self.hunt, "study": self.study, "survey": self.survey, "tinker": self.tinker}

    @classmethod
    def from_dict(cls, data):
        if not data:
            return cls()
        return cls(hunt=data.get("hunt", 0), study=data.get("study", 0), survey=data.get("survey", 0), tinker=data.get("tinker", 0))

    def __repr__(self):
        return f"<Insight(hunt={self.hunt}, study={self.study}, survey={self.survey}, tinker={self.tinker})>"


# Attributes Type is a custom SQLAlchemy TypeDecorator for handling lists of Attributes objects stored as JSON.
class InsightType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        """
        Convert Attributes objects to dictionaries for storage in the database.
        """
        if value is not None and isinstance(value, Insight):
            return value.to_dict()
        return value

    def process_result_value(self, value, dialect):
        """
        Convert dictionaries back to Attributes objects when retrieving from the database.
        """
        if value is not None:
            return Insight.from_dict(value)
        return value


# Use MutableList to track changes in the JSON column
MutableDict.associate_with(InsightType)
