from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class CourseDictionary(Base):
    __tablename__ = "course_dictionaries"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    dictionary_id = Column(Integer, ForeignKey("dictionaries.id"), nullable=False)

    course = relationship("Course", back_populates="dictionaries")
    dictionary = relationship("Dictionary", back_populates="courses")
