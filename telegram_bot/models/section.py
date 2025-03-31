from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    courses = relationship("Course", back_populates="section")
