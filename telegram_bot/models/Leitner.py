import enum
import sqlalchemy

from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from .Base import Base


class StateEnum(enum.Enum):
    BOX1 = "box1"
    BOX2 = "box2"
    BOX3 = "box3"
    BOX4 = "box4"
    BOX5 = "box5"


class Leitner(Base):
    __tablename__ = "leitner"

    id = Column(Integer, primary_key=True, index=True)
    dictionary_id = Column(Integer, ForeignKey("dictionaries.id"), nullable=False)
    state = Column(Enum(StateEnum), default=StateEnum.BOX1, nullable=False)
    telegram_bot_user_id = Column(String, nullable=False)
    review_datetime = Column(DateTime, default=sqlalchemy.func.now(), nullable=False)
    dictionary = relationship("Dictionary", back_populates="leitner")
