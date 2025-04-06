from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from ..models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    leitner_entries = relationship("Leitner", back_populates="user")
    leitner_settings = relationship("UserLeitnerSetting", back_populates="user")