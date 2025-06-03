import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UserProfile, WorkoutPlan
from services.planner_service import generate_workout_plan
from services.progress_service import mark_workout_done, view_weekly_progress
from services.nutrition_service import calculate_nutrition_goals

engine = create_engine('sqlite:///trainsmart.db')
Session = sessionmaker(bind=engine)

def create_user_profile():
    session = Session()
    print("\n Create a new client profile")

    name = input("Name: ")
    age = int(input("Age: "))
    weight = int(input("Weight (kg): "))
    height = int(input("Height (cm): "))
    level = input("Level (beginner / intermediate / advanced): ").lower()
    goal = input("Goal (loss / gain / cardio): ").lower()
    days = input("Available training days (e.g. monday,wednesday,friday): ").lower()
    equipment = input("Available equipment (e.g. dumbbells,mat / none): ").lower()
    activity = input("Activity level (low / moderate / high): ").lower()

    profile = UserProfile(
        name=name,
        age=age,
        weight=weight,
        height=height,
        level=level,
        goal=goal,
        available_days=days,
        equipment=equipment,
        activity=activity
    )

    session.add(profile)
    session.commit()
    print(f" Client '{name}' created successfully. ID: {profile.id}")

def view_workout_plan():
    session = Session()
    user_id = int(input("Enter client ID: "))
    plans = session.query(WorkoutPlan).filter_by(user_id=user_id).all()

    if not plans:
        print("No workout plan found. Create one first.")
        return

    print(f"\n Weekly Plan for Client {user_id}:")
    for plan in plans:
        print(f"{plan.day:<10} | {plan.workout_description}")

def list_all_clients():
    session = Session()
    users = session.query(UserProfile).all()

    print("\n List of all clients:")
    if not users:
        print("No clients found.")
    else:
        for user in users:
            print(f"ID: {user.id} | {user.name} | Goal: {user.goal} | Level: {user.level}")

def main_menu():
    while True:
        print("\n=== TrainSmart CLI (Coach Mode) ===")
        print("1. Create New Client Profile")
        print("2. Create Workout Plan for Client")
        print("3. View Client's Workout Plan")
        print("4. Mark Client Workout as Done")
        print("5. View Client Weekly Progress")
        print("6. View Client Daily Nutrition Recommendations")
        print("7. Exit")
        print("8. List All Clients")

        choice = input("Select an option: ")

        if choice == '1':
            create_user_profile()
        elif choice == '2':
            user_id = int(input("Enter client ID: "))
            generate_workout_plan(user_id)
        elif choice == '3':
            view_workout_plan()
        elif choice == '4':
            user_id = int(input("Enter client ID: "))
            day = input("Enter the day to mark as done (e.g. monday): ")
            mark_workout_done(user_id, day)
        elif choice == '5':
            user_id = int(input("Enter client ID: "))
            view_weekly_progress(user_id)
        elif choice == '6':
            user_id = int(input("Enter client ID: "))
            session = Session()
            user = session.query(UserProfile).filter_by(id=user_id).first()
            if user:
                calculate_nutrition_goals(user)
            else:
                print("Client not found.")
        elif choice == '7':
            print(" Goodbye, Stay strong.")
            sys.exit()
        elif choice == '8':
            list_all_clients()
        else:
            print(" Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
