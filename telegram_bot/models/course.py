from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    sections = relationship("Section", back_populates="course")
    leitner_settings = relationship("UserLeitnerSetting", back_populates="course")