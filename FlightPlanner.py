from fastapi import requests
import re
import requests
import pandas as pd
from ast import literal_eval
import os
from dotenv import load_dotenv
from datetime import datetime

AIRLINE_NAMES = {
    "B6": "JetBlue Airways",
    "DL": "Delta Air Lines",
    "AA": "American Airlines",
    "UA": "United Airlines",
    "AS": "Alaska Airlines"
}

load_dotenv()
flight_id = os.getenv("FLIGHT_KEY")
flight_secret = os.getenv("FLIGHT_SECRET")

def parse_llm_output_flight(output):
    rationale = "Thought: " + output.split("Flight suggestions:")[0]
    key_points = output.split("Flight suggestions:")[1]
    output = key_points.replace("    ", "").replace("I hope that helps!", "").strip()
    parsed_output = literal_eval(output)
    dataframe = pd.DataFrame.from_dict(parsed_output)
    return dataframe, rationale

def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"  # Use this for the test environment
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": flight_id,
        "client_secret": flight_secret
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None


def get_real_time_flights(departure_city, arrival_city, departure_date):
    api_key = get_access_token()

    if not api_key:
        return []

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": departure_city,
                "destinationLocationCode": arrival_city,
                "departureDateTimeRange": {"date": departure_date}
            }
        ],
        "travelers": [{"id": "1", "travelerType": "ADULT"}],
        "sources": ["GDS"],
        "searchCriteria": {
            "maxFlightOffers": 5
        }
    }

    response = requests.post(url, headers=headers, json=data)  # Note: POST request

    if response.status_code != 200:
        return []

    flights = response.json().get("data", [])
    flight_data = []

    for flight in flights:
        for offer in flight["itineraries"]:
            if len(offer["segments"]) == 1:
                seg = offer["segments"][0]

                flight_price = float(flight["price"]["total"])
                departure_time = datetime.strptime(seg["departure"]["at"], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
                arrival_time = datetime.strptime(seg["arrival"]["at"], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
                airline_code = seg["carrierCode"]
                airline_name = AIRLINE_NAMES.get(airline_code, airline_code)

                flight_info = {
                    "departure_city": seg["departure"]["iataCode"],
                    "arrival_city": seg["arrival"]["iataCode"],
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "airline": airline_name,
                    "flight_price": flight_price
                }
                flight_data.append(flight_info)

    return flight_data

def extract_iata_code(city_field):
    match = re.search(r"\((\w{3})\)", city_field)
    if match:
        return match.group(1)  # Return the 3-letter code inside the parentheses
    return None


def extract_cities_from_dataframe(dataframe):
    if not dataframe.empty:
        departure_city_field = dataframe.iloc[0]["departure_city"]
        arrival_city_field = dataframe.iloc[0]["arrival_city"]
        departure_iata = extract_iata_code(departure_city_field)
        arrival_iata = extract_iata_code(arrival_city_field)
        return departure_iata, arrival_iata
    return None, None

def extract_date_from_dataframe(dataframe):
    if not dataframe.empty:
        return dataframe.iloc[0]["departure_date"]
    return None

def parse_flight_output(current_output, description):
    dataframe, rationale = parse_llm_output_flight(current_output)
    print(rationale)

    error = False
    departure_city, arrival_city = extract_cities_from_dataframe(dataframe)
    if not departure_city or not arrival_city:
        error = True

    departure_date = extract_date_from_dataframe(dataframe)
    if not departure_date:
        error = True

    real_time_flights = get_real_time_flights(departure_city, arrival_city, departure_date)
    if len(real_time_flights) != 0 and error == False:
        dataframe = pd.DataFrame(real_time_flights)


    print("\nFlight Suggestions (Direct Flights Only):\n")
    plan = ""
    for _, row in dataframe.iterrows():
        flight_details = (
                "Flight from " + row['departure_city'] + " to " + row['arrival_city'] + ":\n"
                "- Airline: " + row['airline'] + "\n"
                "- Departure: " + row['departure_time'] + "\n"
                "- Arrival: " + row['arrival_time'] + "\n"
                "- Price: $" + "{:,.2f}".format(
            row['flight_price']) + "\n"
        )

        print(flight_details)
        plan += flight_details

    return plan
