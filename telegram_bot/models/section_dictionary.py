import sqlalchemy

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class SectionDictionary(Base):
    __tablename__ = "section_dictionaries"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    dictionary_id = Column(Integer, ForeignKey("dictionaries.id"), nullable=False)

    section = relationship("Section", back_populates="dictionaries")
    dictionary = relationship("Dictionary", back_populates="sections")

    __table_args__ = (
        sqlalchemy.UniqueConstraint('section_id', 'dictionary_id', name='uix_section_dictionary'),
    )
