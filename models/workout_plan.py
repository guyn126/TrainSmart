from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .user_profile import UserProfile

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    day = Column(String)
    workout_description = Column(String)

    user = relationship("UserProfile", back_populates="workout_plans")
