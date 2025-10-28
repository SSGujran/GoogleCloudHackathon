import os
from dotenv import load_dotenv

# Load environment variables from a .env file (recommended for secrets)
load_dotenv()

# --- Google Cloud/Gemini Setup ---
# Project ID mentioned in the document for context (do not use for authentication unless necessary)
GCP_PROJECT_ID = 'qwiklabs-gcp-04-ae07a641f370'

# Gemini API Key (or rely on Google Cloud Service Accounts for Vertex AI)
GEMINI_API_KEY = os.getenv("AIzaSyDjJuWWGMW_uxZ1yp61TcSLKLfPhnlCmf4")

# --- Agent/Location Setup ---
# The specific city/neighborhood the agent is monitoring
TARGET_CITY = "Rotterdam, Netherlands"

# Example API Key for a third-party weather service (Replace with your own)
# For a real MVP, you'd use a free weather API like OpenWeatherMap
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Example URL for a public city data feed (e.g., city incidents, roadworks)
# This will likely be a real, complex endpoint in a production scenario
CITY_DATA_API_URL = "https://example-city-opendata.com/api/v1/incidents"