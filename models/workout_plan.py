from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    day = Column(String, nullable=False)             
    workout_description = Column(String, nullable=False)  

    user = relationship("UserProfile", backref="plans")

    def __repr__(self):
        return f"<WorkoutPlan(day={self.day}, workout='{self.workout_description}')>"
