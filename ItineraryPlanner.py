import asyncio
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from ast import literal_eval
import pandas as pd
import numpy as np
import re

def parse_llm_output_itinerary(output):
    rationale = "Thought: " + output.split("Key points:")[0]
    key_points = output.split("Key points:")[1]
    output = key_points.replace("    ", "").replace("I hope that helps!", "").strip()
    parsed_output = literal_eval(output)
    dataframe = pd.DataFrame.from_dict(parsed_output)
    return dataframe, rationale

async def geocode_address(address, retries=3):
    async with Nominatim(user_agent="Custom-Trip-Planner-1.0", adapter_factory=AioHTTPAdapter) as geolocator:
        for i in range(retries):
            try:
                location = await geolocator.geocode(address, timeout=10)
                if location:
                    return {'lat': location.latitude, 'lon': location.longitude}
                return None
            except Exception as e:
                if "429" in str(e):
                    # Handle rate limit (HTTP 429)
                    wait_time = 2 ** i
                    await asyncio.sleep(wait_time)
                else:
                    # Handle other exceptions
                    return None
        # If retries are exhausted, return None
        return None

async def ageocode_addresses(addresses):
    tasks = [geocode_address(address) for address in addresses]
    locations = await asyncio.gather(*tasks)
    return locations

def geocode_addresses(addresses):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    result = loop.run_until_complete(ageocode_addresses(addresses))
    return result

def extract_num_days_from_prompt(description):
    match = re.search(r'(\d+)\s*(day|days|week|weeks)', description.lower())
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        if 'day' in unit:
            return number
        elif 'week' in unit or 'weekly' in unit:
            return number * 7
    else:
        return 5 # Assumes it is a 5-day trip

def split_trip_into_days(dataframe, num_days):
    day_splits = np.array_split(dataframe.index, num_days)
    days = {}
    day_number = 1

    for split in day_splits:
        days[f"Day {day_number}"] = dataframe.loc[split]
        day_number += 1

    return days

def parse_plan_output(current_output, description):
    # Parse the output
    dataframe, rationale = parse_llm_output_itinerary(current_output)
    print(rationale)

    # Geocode the addresses
    coordinates = geocode_addresses(dataframe["name"])
    dataframe["lat"] = [cords["lat"] if cords else None for cords in coordinates]
    dataframe["lon"] = [cords["lon"] if cords else None for cords in coordinates]

    # Split the trip into days
    num_days = extract_num_days_from_prompt(description)
    days = split_trip_into_days(dataframe, num_days)

    # Display the trip plan, split by days
    plan = ""
    for day, activities in days.items():
        print(f"\n{day}:\n")
        plan += f"\n{day}:\n"
        for _, row in activities.iterrows():
            print(
                f"Location: {row['name']}\nDescription: {row['description']}\nCoordinates: ({row['lat']}, {row['lon']})\n")
            plan += f"Location: {row['name']}\nDescription: {row['description']}\nCoordinates: ({row['lat']}, {row['lon']})\n"

    return plan
