from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from ..models.base import Base


class User(Base):
    __tablename__ = "users"

    telegram_user_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)

    leitner_entries = relationship("Leitner", back_populates="user")