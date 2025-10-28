# orchestrator.py

import time
import logging
import json  # Used for pretty printing the final output
from sensor_agent import SensorAgent
from messenger_agent import MessengerAgent
from db_tools import initialize_db, fetch_recent_data  # Need fetch_recent_data now
from config import GCP_PROJECT_ID  # Assumes config.py exists and is minimal

# --- Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Orchestrator')

# --- Agent Initialization ---
try:
    sensor_agent = SensorAgent()
    messenger_agent = MessengerAgent()
except ImportError as e:
    logger.error(f"Failed to import an agent or tool: {e}")
    exit(1)


# --- Core Workflow Function ---

def run_neighborhood_watch_cycle(city_to_monitor: str = "Amsterdam"):
    """
    Executes the autonomous agent cycle: Perceive (Sensor) -> Act (Messenger).
    """
    logger.info("--- STARTING NEW NEIGHBORHOOD WATCH CYCLE ---")

    # 1. PERCEIVE: Sensor Agent collects and packages raw data
    logger.info("Step 1: Sensor Agent is collecting and packaging raw data...")
    try:
        raw_data_package = sensor_agent.perceive(city=city_to_monitor)

        if not raw_data_package or all(not v for v in raw_data_package.values()):
            logger.warning("Sensor Agent returned an empty or insufficient data package. Aborting cycle.")
            return

    except Exception as e:
        logger.error(f"Sensor Agent failed during perception: {e}")
        return

    # 2. ACT/PRESENT: Messenger Agent publishes the raw package
    logger.info("Step 2: Messenger Agent is publishing the raw data package...")
    try:
        publication_status = messenger_agent.act(raw_data_package)
        logger.info(f"Cycle completed. Publication Status: {publication_status}")

    except Exception as e:
        logger.error(f"Messenger Agent failed during publication: {e}")
        return

    logger.info("--- CYCLE COMPLETED SUCCESSFULLY ---")


# --- Main Execution and Display ---

if __name__ == '__main__':

    # 0. Initialize Database Connection (ensures the data file exists)
    if not initialize_db():
        logger.critical("Failed to initialize local file storage. Cannot proceed.")
        exit(1)

    # 1. Run the Agent Cycle Once
    run_neighborhood_watch_cycle(city_to_monitor="My Local Neighborhood")

    # 2. Fetch and Display the Results
    print("\n" + "=" * 80)
    print("📢 NEIGHBORHOOD WATCH ALERT DISPLAY 📢")
    print("=" * 80)

    # Fetch the latest record (limit=1)
    latest_data = fetch_recent_data(limit=1)

    if latest_data:
        record = latest_data[0]

        print(f"\n✅ SUCCESS: Retrieved Data Package from ID: {record['id']}")
        print(f"   Published Time: {record['timestamp']}")
        print(f"   Monitored Location: {record['payload'].get('monitoring_location')}")
        print("\n--- RAW DATA PAYLOAD ---")

        # Print the raw data payload in a readable JSON format
        print(json.dumps(record['payload'], indent=4))

    else:
        print("\n❌ FAILURE: Could not retrieve data after running the agent cycle. Check logs.")

    print("\n" + "=" * 80)