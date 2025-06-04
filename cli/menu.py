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
    print("\n🣍 Create a new client profile")

    name = input("Name: ")
    age = int(input("Age: "))
    weight = int(input("Weight (kg): "))
    height = int(input("Height (cm): "))

    valid_levels = ["beginner", "intermediate", "advanced"]
    level = input("Level (beginner / intermediate / advanced): ").lower()
    while level not in valid_levels:
        level = input(" Invalid level. Choose: beginner / intermediate / advanced: ").lower()

    valid_goals = ["loss", "gain", "cardio"]
    goal = input("Goal (loss / gain / cardio): ").lower()
    while goal not in valid_goals:
        goal = input(" Invalid goal. Choose: loss / gain / cardio: ").lower()

    days = input("Available training days:").lower()

    valid_equipment = ["no_equipment", "dumbbells"]
    equipment = input("Available equipment (no_equipment / dumbbells): ").lower()
    while equipment not in valid_equipment:
        equipment = input(" Invalid equipment. Choose: no_equipment / dumbbells: ").lower()

    valid_activity = ["low", "moderate", "high"]
    activity = input("Activity level (low / moderate / high): ").lower()
    while activity not in valid_activity:
        activity = input(" Invalid activity level. Choose: low / moderate / high: ").lower()

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
    plans = session.query(WorkoutPlan).filter_by(user_id=user_id).order_by(WorkoutPlan.day).all()

    if not plans:
        print(" No workout plan found. Create one first.")
        return

    print(f"\n Weekly Plan for Client {user_id}:\n")

    for plan in plans:
        print(f"{plan.day.capitalize():<10} | {plan.workout_description}")

def mark_workout_as_done():
    session = Session()
    user_id = int(input("Enter client ID: "))
    workouts = session.query(WorkoutPlan).filter_by(user_id=user_id).all()

    if not workouts:
        print(" This client has no workout plan yet.")
        return

    available_days_map = {w.day.strip().lower(): w.day.strip() for w in workouts}
    print(f"\n Available days for Client {user_id}: {', '.join(available_days_map.values())}")

    day_input = input("Enter the day(s) to mark as done (e.g. monday or wednesday,friday): ").lower().replace(" ", "")
    day_list = day_input.split(",")

    matched = False
    for day in day_list:
        if day in available_days_map:
            real_day = available_days_map[day]
            mark_workout_done(user_id, real_day)
            print(f" {real_day} marked as done.")
            matched = True
        else:
            print(f" '{day}' is not in the plan. Please try again.")

    if not matched:
        print(" No valid day was marked.")

def list_all_clients():
    session = Session()
    users = session.query(UserProfile).all()

    print("\n List of all clients:")
    if not users:
        print("No clients found.")
    else:
        for user in users:
            print(f"ID: {user.id} | {user.name} | Goal: {user.goal} | Level: {user.level}")

def export_plan_to_txt():
    import os
    session = Session()
    user_id = int(input("Enter client ID: "))
    user = session.query(UserProfile).filter_by(id=user_id).first()
    plans = session.query(WorkoutPlan).filter_by(user_id=user_id).order_by(WorkoutPlan.day).all()

    if not user or not plans:
        print(" Cannot export: client or plan not found.")
        return

    if not os.path.exists("plans"):
        os.makedirs("plans")

    filename = f"plans/user_{user_id}_plan.txt"
    with open(filename, "w") as file:
        file.write(f" Weekly Plan for {user.name} (Client ID {user.id})\n")
        for plan in plans:
            file.write(f"{plan.day:<10} | {plan.workout_description}\n")

    print(f" Plan exported to {filename}")

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
        print("9. Export Client Workout Plan (.txt)")

        choice = input("Select an option: ")

        if choice == '1':
            create_user_profile()
        elif choice == '2':
            user_id = int(input("Enter client ID: "))
            generate_workout_plan(user_id)
        elif choice == '3':
            view_workout_plan()
        elif choice == '4':
            mark_workout_as_done()
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
        elif choice == '9':
            export_plan_to_txt()
        else:
            print(" Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
