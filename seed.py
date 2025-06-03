from sqlalchemy import create_engine
from models import Base
from models.user_profile import UserProfile
from models.workout_plan import WorkoutPlan

# Create SQLite database file
engine = create_engine('sqlite:///trainsmart.db')

# Drop and recreate all tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

print(" Database initialized successfully.")

# Optional: Create a sample user
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

sample_user = UserProfile(
    name="Alex",
    age=30,
    weight=75,
    height=175,
    level="intermediate",
    goal="perte",
    available_days="monday,wednesday,friday",
    equipment="dumbbells,mat",
    activity="moderate"
)

session.add(sample_user)
session.commit()

print(f" Sample user created: {sample_user.name} (ID: {sample_user.id})")
