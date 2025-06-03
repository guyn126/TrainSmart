def calculate_nutrition_goals(profile):
    weight = profile.weight
    height = profile.height
    age = profile.age
    goal = profile.goal
    activity = profile.activity

    # Basal Metabolic Rate (Harris-Benedict)
    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    # Activity level multiplier
    activity_factors = {
        "low": 1.2,
        "moderate": 1.55,
        "high": 1.75
    }
    tdee = bmr * activity_factors.get(activity, 1.55)

    # Adjust for goal
    if goal == "perte":
        tdee -= 500
    elif goal == "gain":
        tdee += 300
    # maintain: no change

    # Macronutrient breakdown: 30% protein / 50% carbs / 20% fat
    protein_g = int((tdee * 0.3) / 4)
    carbs_g = int((tdee * 0.5) / 4)
    fat_g = int((tdee * 0.2) / 9)

    print(f"\n Nutrition Recommendations for {profile.name}")
    print(f"Calories: {int(tdee)} kcal/day")
    print(f"- Protein: {protein_g} g")
    print(f"- Carbs:   {carbs_g} g")
    print(f"- Fat:     {fat_g} g")

    print("\n Sample food ideas:")
    if goal == "perte":
        print("- Grilled chicken with vegetables")
        print("- Greek yogurt and berries")
        print("- Oats with almond milk")
    elif goal == "gain":
        print("- Rice and beef stir-fry")
        print("- Protein smoothie with peanut butter")
        print("- Eggs, toast and avocado")
    elif goal == "cardio":
        print("- Banana + oatmeal pre-workout")
        print("- Fish, rice and greens")
        print("- Pasta with lean meat")

