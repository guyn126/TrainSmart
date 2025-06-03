from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import UserProfile, WorkoutPlan, Base
from services.exercise_db import exercise_library
import random

engine = create_engine('sqlite:///trainsmart.db')
Session = sessionmaker(bind=engine)

def generate_workout_plan(user_id):
    session = Session()
    user = session.query(UserProfile).filter_by(id=user_id).first()

    if not user:
        print(" User not found.")
        return

    print(f"\n Generating plan for {user.name}...")

    # Clear existing plan
    session.query(WorkoutPlan).filter_by(user_id=user_id).delete()

    goal = user.goal
    level = user.level
    available_days = user.available_days.lower().split(",")
    equipment_list = user.equipment.lower().split(",")

    plan = []

    for day in available_days:
        selected_equipment = "no_equipment"
        if "dumbbells" in equipment_list:
            selected_equipment = "dumbbells"

        # Fallback logic
        try:
            exercises = exercise_library[goal][level][selected_equipment]
        except KeyError:
            print(f" No matching workout found for {goal} / {level} / {selected_equipment}")
            continue

        workout = random.choice(exercises)
        plan.append(WorkoutPlan(user_id=user.id, day=day.capitalize(), workout_description=workout))

    session.add_all(plan)
    session.commit()
    print(" Weekly workout plan created.")
