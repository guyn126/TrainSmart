from sqlalchemy import Column, Integer, String
from models.base import Base

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    weight = Column(Integer)       # en kg
    height = Column(Integer)       # en cm
    level = Column(String)         # débutant / intermédiaire / avancé
    goal = Column(String)          # perte / gain / cardio
    available_days = Column(String)  # ex : "lundi,mercredi,vendredi"
    equipment = Column(String)     # ex : "haltères,tapis"
    activity = Column(String)      # low / moderate / high

    def __repr__(self):
        return f"<UserProfile(name={self.name}, goal={self.goal}, level={self.level})>"
