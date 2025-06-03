from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import UserProfile, WorkoutPlan
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

    # Clear previous plan
    session.query(WorkoutPlan).filter_by(user_id=user.id).delete()

    goal = user.goal
    level = user.level
    available_days = user.available_days.lower().split(",")
    equipment_list = user.equipment.lower().split(",")

    plan = []

    for day in available_days:
        selected_equipment = "no_equipment"
        if "dumbbells" in equipment_list:
            selected_equipment = "dumbbells"

        try:
            exercises = exercise_library[goal][level][selected_equipment]
        except KeyError:
            print(f" No matching workout found for {goal} / {level} / {selected_equipment}")
            continue

        daily_exercises = random.sample(exercises, min(4, len(exercises)))
        workout_description = ", ".join(daily_exercises)

        plan.append(
            WorkoutPlan(
                user_id=user.id,
                day=day.strip().capitalize(),
                workout_description=workout_description
            )
        )

    session.add_all(plan)
    session.commit()
    print(" Weekly workout plan created.")
