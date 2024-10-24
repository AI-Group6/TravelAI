from flask import Flask, request, jsonify
from postgresConnection import *
import getpass
from FlightPlanner import *
from ItineraryPlanner import *
from LodgingPlanner import *
from LLaMaTravelAI import *
from PhiLocalAI import *
from flask_cors import CORS
from Parsing import  *

app = Flask(__name__)
CORS(app)

def run_trip_planner(loggedUser, description, greeting):
    if greeting:
        current_output = ""
        prompt = description
        for output in generateGreeting(prompt):
            current_output += output
        print(current_output)
        postHistory(user_login=loggedUser, title_message=description, ai_response=current_output)
        return current_output

    else:
        print(f"Generating trip plan for: {description}\n")

        try:
            # Try to generate key points from API
            current_output = ""
            for output in generate_key_itinerary_points(description):
                current_output += output

            plan = parse_plan_output(current_output, description)
        except Exception:
            # Cannot generate output locally that breaks it up into days, too resource intensive and not possible
            plan = get_trip_planning_suggestions_local(description)

        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=plan)

        return plan

def run_flight_planner(loggedUser, description, greeting):
    current_output = ""
    if greeting:
        for output in generateGreeting(description):
            current_output += output
        print(current_output)
        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=current_output)
            return current_output

    else:
        print(f"Generating flight plan for: {description}\n")

        try:
            # Generate key points using API
            for output in generate_key_airplane_points(description):
                current_output += output

            plan = parse_flight_output(current_output, description)
        except Exception:
            # Cannot generate output locally that breaks it up into days, too resource intensive and not possible
            plan = get_flight_planning_suggestions_local(description)

        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=plan)

        return plan

def run_lodging_planner(loggedUser, description, greeting):
    current_output = ""
    if greeting:
        for output in generateGreeting(description):
            current_output += output
        print(current_output)
        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=current_output)
        return current_output

    else:
        print(f"Generating hotel plan for: {description}\n")

        try:
            # Generate key hotel points using the LLM
            for output in generate_key_lodging_points(description):
                current_output += output

            # Parse the LLM output for hotel details
            plan = parse_lodging_output(current_output, description)
        except Exception:
            # In case of API failure, fall back to local suggestion generation
            plan = get_lodging_planning_suggestions_local(description)

        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=plan)

        return plan

def run_generic_planner(loggedUser, description, greeting):
    current_output = ""
    if greeting:
        for output in generateGreeting(description):
            current_output += output
        print(current_output)
        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=current_output)
        return current_output

    else:
        print(f"Generating feedback: {description}\n")

        try:
            # Generate key hotel points using the LLM
            for output in generate_generic_travel_prompt(description):
                current_output += output

            print (current_output)
            # Parse the LLM output for hotel details
            plan = current_output
        except Exception:
            # In case of API failure, fall back to local suggestion generation
            plan = get_generic_planning_suggestions_local(description)

        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=plan)
        return plan


@app.route('/run_trip_planner', methods=['POST'])
def trip_planner():
    data = request.json
    logged_user = data.get('loggedUser')
    description = data.get('description')

    if not description:
        return jsonify({'error': 'Missing description'}), 400

    if not logged_user:
        logged_user = "None"

    try:
        initial_state = description.lower().split()
        greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
        plan = run_generic_planner(loggedUser=logged_user, description=description,greeting=greeting_check(greeting_problem))
        return jsonify({'plan': plan}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run_itinerary_planner', methods=['POST'])
def itinerary_planner():
    data = request.json
    logged_user = data.get('loggedUser')
    description = data.get('description')

    if not description:
        return jsonify({'error': 'Missing description'}), 400

    if not logged_user:
        logged_user = "None"

    try:
        initial_state = description.lower().split()
        greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
        plan = run_trip_planner(loggedUser=logged_user, description=description,greeting=greeting_check(greeting_problem))
        return jsonify({'plan': plan}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run_flight_planner', methods=['POST'])
def flight_planner():
    data = request.json
    logged_user = data.get('loggedUser')
    description = data.get('description')

    if not description:
        return jsonify({'error': 'Missing description'}), 400

    if not logged_user:
        logged_user = "None"

    try:
        initial_state = description.lower().split()
        greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
        plan = run_flight_planner(loggedUser=logged_user, description=description,greeting=greeting_check(greeting_problem))
        return jsonify({'plan': plan}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run_lodging_planner', methods=['POST'])
def lodging_planner():
    data = request.json
    logged_user = data.get('loggedUser')
    description = data.get('description')

    if not description:
        return jsonify({'error': 'Missing description'}), 400

    if not logged_user:
        logged_user = "None"

    try:
        initial_state = description.lower().split()
        greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
        plan = run_lodging_planner(loggedUser=logged_user, description=description,greeting=greeting_check(greeting_problem))
        print(plan)
        return jsonify({'plan': plan}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Example command-line interface loop
def main():
    print("Welcome to the AI Trip Planner!")
    choice = input("Would you like to run the command line interface (1) or the Flask server (2)?\n")
    ##normal code
    if choice == "1":
        choice = input("Would you like to login (1), create a new user (2), or not log in (3)?\n")
        if choice == "1":
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            loggedUser = checkLogin(username=username, password=password)
            if loggedUser is None:
                exit()
            else:
                print(f"Welcome, {loggedUser}")

            disp_history = input("Would you like to view your previous chat history?\nYes(y) or No(n)?\n")
            if disp_history == "y":
                history = fetchHistory(loggedUser)
                if history:
                    for entry in history:
                        print(f"{entry['title']}")
                        print(f"{entry['response']}")
                        print(f"{entry['timestamp']}\n")
                else:
                    print("No current chat history.")
            else:
                pass

        elif choice == "2":
            username = input("Please Enter Username: ")
            password = getpass.getpass("Please Choose a Password: ")
            redo_pass = getpass.getpass("Please Confirm Password: ")
            while redo_pass != password:
                password = getpass.getpass("Passwords Do Not Match, Please Try Again: ")
                redo_pass = getpass.getpass("Please Confirm Password: ")
            loggedUser = createUser(username=username, password=password)
            if loggedUser is None:
                exit()
            else:
                print(f"Welcome, {loggedUser}")

        elif choice == "3":
            print("Welcome")

        else:
            print("Invalid choice. Please try again.")
            exit()

        while True:
            plan_type = input("Would you like to create an itinerary (1), find flights (2), find lodging (3), or generic inquiry (4)?\n")
            if plan_type == "1":
                print("\nEnter a trip description:")
                description = input("> ").strip()

                initial_state = description.lower().split()
                greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
                run_trip_planner(loggedUser="None", description=description, greeting=greeting_check(greeting_problem))
            elif plan_type == "2":
                print("\nEnter in which cities you want to fly between:")
                description = input("> ").strip()

                initial_state = description.lower().split()
                greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
                run_flight_planner(loggedUser="None", description=description,greeting=greeting_check(greeting_problem))
            elif plan_type == "3":
                print("\nEnter what city you want to find lodging:")
                description = input("> ").strip()

                initial_state = description.lower().split()
                greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
                run_lodging_planner(loggedUser="None", description=description,greeting=greeting_check(greeting_problem))
            elif plan_type == "4":
                print("\nEnter any travel related questions:")
                description = input("> ").strip()

                initial_state = description.lower().split()
                greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
                run_generic_planner(loggedUser="None", description=description,greeting=greeting_check(greeting_problem))

            print("Do you want to exit (Y/N): ")
            description = input("> ").strip()
            if description.lower() == "y":
                print("\n Hope you have a good trip!")
                break

    # flask interface
    elif choice == "2":
        app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
