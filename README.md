# TrainSmart CLI – Coach Edition

TrainSmart CLI is a smart command-line application designed for fitness coaches to manage multiple clients, create personalised workout plans, and track their progress.


##   Features

 Multi-client management     Create and manage individual profiles for each client                      
 Workout plan generation     Automatically build a weekly plan based on goal, level, availability, etc.
 Completion tracking         Mark workouts as done and track weekly discipline                         
Nutrition recommendations    Calculate daily calorie and macronutrient needs per client                
 Client list overview         View all clients with their ID, goal, and training level                   


###   Set up the environment

pipenv install
pipenv shell


#### Initialize the database

pipenv run python seed.py


# Run the app
pipenv run python run.py
