# agents/messenger_agent.py

import logging
# Assumes tools/db_tools.py has the function to save the data to the database
from db_tools import save_presentation_data

# --- Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MessengerAgent')


class MessengerAgent:
    """
    The Messenger Agent (Act/Present Component).
    Receives the raw data package from the Sensor Agent and publishes it
    directly to the database for the frontend dashboard (Streamlit) to retrieve.
    """

    def __init__(self, role: str = "Data Publisher and Presentation Layer"):
        self.role = role
        logger.info(f"Messenger Agent initialized with role: {self.role}")

    def act(self, raw_data: dict) -> str:
        """
        Publishes the raw, packaged data to the presentation database.

        Args:
            raw_data: A dictionary containing the raw, structured data
                      collected and packaged by the Sensor Agent.

        Returns:
            A string indicating the result of the publishing action.
        """
        if not raw_data:
            logger.warning("Received empty data package. Skipping publishing.")
            return "Skipped: Received empty data."

        # The core action: saving the raw data directly to the database
        logger.info(f"Attempting to publish data package with keys: {list(raw_data.keys())}...")

        try:
            # Call the tool to write the data to the persistent store (e.g., Firestore)
            success = save_presentation_data(raw_data)

            if success:
                message = "SUCCESS: Successfully published raw data package to the presentation database."
                logger.info(message)
                return message
            else:
                message = "FAILURE: Failed to save data to the database (Check db_tools.py and connection)."
                logger.error(message)
                return message

        except ImportError:
            error_message = "ImportError: tools/db_tools.py or save_presentation_data function not found."
            logger.error(error_message)
            return error_message
        except Exception as e:
            error_message = f"RUNTIME ERROR: An unexpected error occurred during data publishing: {type(e).__name__}: {e}"
            logger.error(error_message, exc_info=True)
            return error_message


# --- Example Usage (Requires an implementation of tools/db_tools.py) ---

if __name__ == '__main__':
    # NOTE: This block is for testing. In the final system,
    # the orchestrator.py will call messenger_agent.act()

    # Mock Data from the Sensor Agent
    mock_sensor_output = {
        "timestamp": "2025-10-28T10:40:00Z",
        "source": "Combined Sensor Feed",
        "weather_data": {"city": "Amsterdam", "temp_c": 14, "condition": "Sunny"},
        "incidents_list": [
            {"type": "Road Closure", "location": "Main St", "details": "Expected to last 3 hours."},
            {"type": "Local Event", "location": "Central Park", "details": "Farmers market today."}
        ]
    }

    # Placeholder for db_tools.py mock
    print("--- NOTE: Running in Test Mode - Requires a functional tools/db_tools.py for actual database writes. ---")

    # Example initialization and execution
    # messenger = MessengerAgent()
    # result = messenger.act(mock_sensor_output)
    # print(f"\nFinal Publishing Result: {result}")