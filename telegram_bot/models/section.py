from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    dictionary_file_path = Column(String, nullable=True)

    course = relationship("Course", back_populates="sections")
    dictionaries = relationship("SectionDictionary", back_populates="section")
    leitner_settings = relationship("UserLeitnerSetting", back_populates="section")
