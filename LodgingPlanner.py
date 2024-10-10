import re
import requests
import pandas as pd
from ast import literal_eval
import os
from dotenv import load_dotenv

load_dotenv()
hotel_id = os.getenv("FLIGHT_KEY")
hotel_secret = os.getenv("FLIGHT_SECRET")

# Function to parse LLM output for hotels
def parse_llm_output_lodging(output):
    rationale = "Thought: " + output.split("Hotel suggestions:")[0]
    hotel_points = output.split("Hotel suggestions:")[1]
    output = hotel_points.replace("    ", "").replace("I hope that helps!", "").strip()
    parsed_output = literal_eval(output)
    dataframe = pd.DataFrame.from_dict(parsed_output)
    return dataframe, rationale


# Function to get access token from Amadeus API
def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": hotel_id,
        "client_secret": hotel_secret
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None


# Function to get hotels by city code using Amadeus API
def get_hotels_with_pricing(city_code, check_in_date, check_out_date):
    api_key = get_access_token()

    if not api_key:
        print("Error: Unable to fetch access token")
        return []

    url = "https://test.api.amadeus.com/v2/shopping/hotel-offers"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {
        "cityCode": city_code,
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            return []

        hotels = response.json().get("data", [])
        hotel_data = []

        # Limit to 5 hotels
        for i, hotel in enumerate(hotels):
            if i >= 5:
                break

            hotel_name = hotel.get("hotel", {}).get("name", "N/A")
            price = hotel.get("offers", [])[0].get("price", {}).get("total", "N/A")

            hotel_info = {
                "hotel_name": hotel_name,
                "hotel_price": price
            }
            hotel_data.append(hotel_info)

        return hotel_data
    except Exception as e:
        return []

def extract_dates_from_dataframe(dataframe):
    if not dataframe.empty:
        return dataframe.iloc[0]["arrival_date"], dataframe.iloc[0]["departure_date"]
    return None

def extract_iata_code(city_field):
    match = re.search(r"\((\w{3})\)", city_field)
    if match:
        return match.group(1)
    return None

def extract_city_from_dataframe(dataframe):
    if not dataframe.empty:
        city_field_value = dataframe.iloc[0]["hotel_name"]
        city_iata = extract_iata_code(city_field_value)
        return city_iata
    return None

# Function to parse and print hotel output (similar to flights)
def parse_lodging_output(current_output, description):
    error = False
    dataframe, rationale = parse_llm_output_lodging(current_output)
    print(rationale)

    city_code = extract_city_from_dataframe(dataframe)
    if not city_code:
        error = True

    arrival_date, departure_date = extract_dates_from_dataframe(dataframe)
    if not arrival_date or not departure_date:
        error = True

    real_time_hotels = get_hotels_with_pricing(city_code, arrival_date, departure_date)
    if len(real_time_hotels) != 0 and error == False:
        dataframe = pd.DataFrame(real_time_hotels)

    print("\nHotel Suggestions:\n")

    plan = ""
    for _, row in dataframe.iterrows():
        hotel_details = (
                "Hotel: " + row['hotel_name'] + "\n" +
                "- Arrival Date: " + arrival_date + "\n" +
                "- Departure Date: " + departure_date + "\n" +
                "- Price per night: $" + "{:.2f}".format(row['price_per_night']) + "\n"
        )
        print(hotel_details)
        plan += hotel_details




    return plan