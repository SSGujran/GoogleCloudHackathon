# agents/sensor_agent.py

import logging
import datetime
import random

# NOTE: The actual implementation would import from tools.api_tools
# from tools.api_tools import get_weather, get_city_data

# --- Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SensorAgent')


# --- MOCK API TOOLS (Replace this section with the real tools/api_tools.py import) ---
# Since api_tools.py is not yet available, these functions mock the data retrieval.
def mock_get_weather(city: str) -> dict:
    """Mocks fetching real-time weather data."""
    conditions = ["Sunny", "Partly Cloudy", "Heavy Rain", "Foggy"]
    return {
        "source": "WeatherAPI",
        "city": city,
        "temperature_c": round(random.uniform(5.0, 25.0), 1),
        "condition": random.choice(conditions),
        "wind_speed_kph": random.randint(5, 40)
    }


def mock_get_city_data(city: str) -> list:
    """Mocks fetching local city incidents/roadworks."""
    incidents = [
        {"type": "Roadwork", "location": "Main Street, near City Hall", "details": "Lane closure until 18:00.",
         "impact": "High"},
        {"type": "Event", "location": "Central Park", "details": "Annual kite festival, expect heavy foot traffic.",
         "impact": "Low"},
        {"type": "Minor Incident", "location": "Kerkstraat 45",
         "details": "Police investigating a minor fender-bender.", "impact": "Medium"},
        {"type": "OV Update", "location": "Tram Line 3", "details": "Minor delay due to technical issue.",
         "impact": "Low"},
        None,  # Introduce a possible empty/None entry to simulate failure or absence
    ]
    # Filter out None and return a random selection of 1-3 incidents
    valid_incidents = [i for i in incidents if i is not None]
    return random.sample(valid_incidents, random.randint(1, 3))


# --- End of MOCK API TOOLS ---


class SensorAgent:
    """
    The Sensor Agent (Perceive Component).
    Collects raw data from various external APIs and packages it into a
    single, structured dictionary.
    """

    def __init__(self, role: str = "Expert Data Retrieval Specialist"):
        self.role = role
        logger.info(f"Sensor Agent initialized with role: {self.role}")

    def perceive(self, city: str) -> dict:
        """
        Executes external API calls and consolidates the raw, unstructured data.

        Args:
            city: The primary city/neighborhood to monitor.

        Returns:
            A dictionary containing all collected raw data, packaged for the Messenger Agent.
        """
        logger.info(f"Starting perception cycle for {city}...")

        # 1. Initialize the main data package
        data_package = {
            "fetch_time_utc": datetime.datetime.utcnow().isoformat() + "Z",
            "monitoring_location": city,
            "raw_weather": {},
            "raw_incidents": [],
            "raw_ov_updates": []  # Placeholder for future data streams
        }

        # 2. Fetch Weather Data (using mock)
        try:
            # In production: weather_data = get_weather(city)
            weather_data = mock_get_weather(city)
            data_package["raw_weather"] = weather_data
            logger.info(f"Fetched weather: {weather_data.get('condition')}, {weather_data.get('temperature_c')}C")
        except Exception as e:
            logger.error(f"Failed to fetch weather data: {e}")
            data_package["raw_weather"] = {"error": str(e)}

        # 3. Fetch City Incidents/Events (using mock)
        try:
            # In production: city_incidents = get_city_data(city)
            city_incidents = mock_get_city_data(city)
            data_package["raw_incidents"] = city_incidents
            logger.info(f"Fetched {len(city_incidents)} raw incidents/events.")
        except Exception as e:
            logger.error(f"Failed to fetch city incidents data: {e}")
            data_package["raw_incidents"] = [{"error": str(e)}]

        # 4. Final Data Validation and Packaging
        if not data_package["raw_weather"] and not data_package["raw_incidents"]:
            logger.warning("No data was successfully retrieved in this cycle.")

        logger.info("Raw data collection complete. Returning packaged data.")
        return data_package


# --- Example Usage (Testing) ---
if __name__ == '__main__':
    print("--- Running Sensor Agent Test ---")

    sensor = SensorAgent()

    # Run a test perception cycle
    test_city = "Amsterdam"
    data_output = sensor.perceive(city=test_city)

    print("\n--- Final Data Package Structure ---")
    print(f"Fetch Time: {data_output.get('fetch_time_utc')}")
    print(f"Monitoring: {data_output.get('monitoring_location')}")
    print(f"Weather Keys: {list(data_output['raw_weather'].keys())}")
    print(f"Incident Count: {len(data_output['raw_incidents'])}")

    # print("\nFull Data Output:")
    # import json
    # print(json.dumps(data_output, indent=2))