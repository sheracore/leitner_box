import sqlalchemy
import enum

from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship

from .base import Base


class LanguageChoice(enum.Enum):
    EN = "en"


class Dictionary(Base):
    __tablename__ = "dictionaries"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(Enum(LanguageChoice), default=LanguageChoice.EN, nullable=False)
    word = Column(String, nullable=False)
    meaning = Column(String, nullable=False)

    sections = relationship("SectionDictionary", back_populates="dictionary")
    leitner = relationship("Leitner", back_populates="dictionary")

    __table_args__ = (
        sqlalchemy.UniqueConstraint('language', 'word', name='uix_language_word'),
    )
