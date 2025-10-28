import requests
from config import WEATHER_API_KEY, WEATHER_API_URL, TARGET_CITY, CITY_DATA_API_URL
import json


def get_weather_data(city_name: str = TARGET_CITY) -> str:
    """
    Fetches current weather data for the specified city.

    Args:
        city_name: The city to fetch weather for. Defaults to TARGET_CITY.

    Returns:
        A JSON string containing the raw weather data.
    """
    print(f"-> Fetching weather data for {city_name}...")

    params = {
        'q': city_name,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Use Celsius
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Return a string representation of the data for the next agent
        return json.dumps(response.json(), indent=2)

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Failed to fetch weather data: {e}"})


def get_city_incident_data() -> str:
    """
    Fetches raw data from the city's open data portal (e.g., incidents, roadworks).

    Returns:
        A JSON string containing the raw incident data.
    """
    print(f"-> Fetching city incident data from {CITY_DATA_API_URL}...")

    # NOTE: In a real scenario, this API might require specific headers or keys.
    # This example simulates a successful raw data fetch.

    try:
        # Simulate fetching actual data with location/description
        response = requests.get(CITY_DATA_API_URL)
        response.raise_for_status()

        # Simulate a typical response from a city data API
        simulated_data = [
            {"id": "I101", "type": "ROADWORK", "status": "PLANNED", "location": "Kerkstraat near #25",
             "details": "Major road resurfacing scheduled for tomorrow, 08:00 - 18:00."},
            {"id": "I102", "type": "INCIDENT", "status": "ACTIVE", "location": "Vondelpark West entrance",
             "details": "Police activity reported, area secured. Possible traffic delays."},
            {"id": "I103", "type": "ROADWORK", "status": "COMPLETE", "location": "Old Town Bridge",
             "details": "Bridge repair finished yesterday."},
            {"id": "I104", "type": "EVENT", "status": "ACTIVE", "location": "Museumplein",
             "details": "Local market running all day today."}
        ]

        return json.dumps(simulated_data, indent=2)

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Failed to fetch city data: {e}"})



# Placeholder function for proximity checking
def check_proximity_score(raw_data: str) -> float:
    """
    Simulates checking if an event mentioned in raw_data is close
    to the neighborhood center (not truly implemented here,
    but provides a tool for the Analyst Agent to use).

    Returns a float score (0.0 to 1.0) or simply True/False for locality.
    """

    # In a real implementation, this would parse location (Lat/Lon) from the raw_data
    # and calculate the distance to the center (e.g., using Haversine formula).

    # For this demonstration, we assume the LLM handles the relevance reasoning
    # based on the text provided, so this tool is minimized.

    if "Kerkstraat" in raw_data or "Flood" in raw_data:
        # Assume these events are highly local and critical
        return 0.9

    return 0.3  # Assume low proximity for other items