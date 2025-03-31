from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .Base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)

    section = relationship("Section", back_populates="courses")
    dictionaries = relationship("CourseDictionary", back_populates="course")
