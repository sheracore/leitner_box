import sqlalchemy
import enum

from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class LanguageChoice(enum.Enum):
    EN = "en"
    FR = "fr"


class Dictionary(Base):
    __tablename__ = "dictionaries"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(Enum(LanguageChoice, create_type=False), default=LanguageChoice.EN, nullable=False)
    word = Column(String, nullable=False)
    meaning = Column(String, nullable=False)

    sections = relationship("SectionDictionary", back_populates="dictionary")
    leitner = relationship("Leitner", back_populates="dictionary")
    examples = relationship("DictionaryExample", back_populates="dictionary", cascade="all, delete-orphan")

    __table_args__ = (
        sqlalchemy.UniqueConstraint('language', 'word', name='uix_language_word'),
    )

class DictionaryExample(Base):
    __tablename__ = "dictionary_examples"

    id = Column(Integer, primary_key=True, index=True)
    dictionary_id = Column(Integer, ForeignKey("dictionaries.id"), nullable=False)
    example = Column(String, nullable=False)

    dictionary = relationship("Dictionary", back_populates="examples")