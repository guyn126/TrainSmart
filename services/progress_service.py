from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import WorkoutPlan
from datetime import datetime

engine = create_engine('sqlite:///trainsmart.db')
Session = sessionmaker(bind=engine)

# This function lets the user mark a workout as done
def mark_workout_done(user_id, day):
    session = Session()
    plan = session.query(WorkoutPlan).filter_by(user_id=user_id, day=day.capitalize()).first()

    if not plan:
        print(" No workout found for that day.")
        return

    # We simply update the description with a marker [DONE]
    if "[DONE]" not in plan.workout_description:
        plan.workout_description += " [DONE]"
        session.commit()
        print(f" Marked {day} workout as completed.")
    else:
        print("ℹ Workout already marked as done.")

# This function gives stats for how many workouts were completed
def view_weekly_progress(user_id):
    session = Session()
    plans = session.query(WorkoutPlan).filter_by(user_id=user_id).all()

    if not plans:
        print("No workout plan found.")
        return

    total = len(plans)
    completed = sum(1 for p in plans if "[DONE]" in p.workout_description)

    if total == 0:
        print(" No scheduled workouts this week.")
    else:
        percentage = int((completed / total) * 100)
        print(f" Weekly completion: {completed}/{total} sessions ({percentage}%)")
