# from sqlalchemy.types import TypeDecorator, JSON
# from sqlalchemy.ext.mutable import MutableDict
#
# class Experience:
#     def __init__(self, current=0, maximum=0):
#         self.current = current
#         self.maximum = maximum
#
#     def to_dict(self):
#         return {"current": self.current, "maximum": self.maximum}
#
#     @classmethod
#     def from_dict(cls, data):
#         return cls(current=data.get("current", 0), maximum=data.get("maximum", 0))
#
#     def __repr__(self):
#         return f"<Experience(current={self.current}, maximum={self.maximum})>"
#
# class ExperienceType(TypeDecorator):
#     impl = JSON
#
#     def process_bind_param(self, value, dialect):
#         if value is not None and isinstance(value, Experience):
#             return value.to_dict()
#         return value
#
#     def process_result_value(self, value, dialect):
#         if value is not None:
#             return Experience.from_dict(value)
#         return value
#
# MutableDict.associate_with(ExperienceType)

