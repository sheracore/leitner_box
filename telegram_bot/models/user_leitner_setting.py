import sqlalchemy
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from telegram_bot.models.base import Base


class UserLeitnerSetting(Base):
    __tablename__ = 'user_leitner_settings'

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.id'), nullable=False)

    user = relationship("User", back_populates='leitner_settings')
    course = relationship("Course", back_populates='leitner_settings')
    section = relationship("Section", back_populates='leitner_settings')

    __table_args__ = (
        sqlalchemy.UniqueConstraint('user_id', 'course_id', 'section_id', name='uix_user_course_section'),
    )