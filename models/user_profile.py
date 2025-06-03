from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
    level = Column(String)
    goal = Column(String)
    available_days = Column(String)
    equipment = Column(String)
    activity = Column(String)

    workout_plans = relationship("WorkoutPlan", back_populates="user")
