# tools/db_tools.py - Updated to use local JSON file storage (No Firestore)

import os
import json
import datetime
import logging

# --- Configuration ---
# File path for persistent storage
DB_FILE_PATH = 'GoogleCloudHackathon/data/alerts.json'
logger = logging.getLogger('DBTools')
logger.setLevel(logging.INFO)


def initialize_db():
    """
    Initializes the local file system storage.
    Creates the necessary directory and the data file if it doesn't exist.
    """
    try:
        # 1. Create the data directory if it doesn't exist
        os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)

        # 2. Check if the file exists and initialize it as an empty JSON list if not
        if not os.path.exists(DB_FILE_PATH) or os.path.getsize(DB_FILE_PATH) == 0:
            with open(DB_FILE_PATH, 'w') as f:
                json.dump([], f)
            logger.info(f"Local database file created at: {DB_FILE_PATH}")
        else:
            logger.info(f"Local database file already exists at: {DB_FILE_PATH}")

        return True

    except Exception as e:
        logger.error(f"Error initializing local file storage: {e}", exc_info=True)
        return False


def save_presentation_data(data: dict) -> bool:
    """
    Saves the structured raw data package to the local JSON file.

    Args:
        data: The dictionary containing the raw, packaged data from the Sensor Agent.

    Returns:
        True if the data was successfully saved, False otherwise.
    """
    if not initialize_db():
        return False

    try:
        # Add metadata required for sorting (since we don't have Firestore's SERVER_TIMESTAMP)
        record = {
            "fetch_timestamp": datetime.datetime.now().isoformat(),
            "raw_payload": data,
            "published_by": "MessengerAgent",
            "id": datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")  # Simple unique ID
        }

        # Read all existing records
        with open(DB_FILE_PATH, 'r') as f:
            all_records = json.load(f)

        # Append the new record and write back
        all_records.append(record)

        # Keep the file size manageable by only storing the last 100 records
        # This prevents the file from growing indefinitely in a loop
        all_records = all_records[-100:]

        with open(DB_FILE_PATH, 'w') as f:
            json.dump(all_records, f, indent=4)

        logger.info(f"Data saved successfully to {DB_FILE_PATH}.")
        return True

    except Exception as e:
        logger.error(f"Failed to save data to local JSON file: {e}", exc_info=True)
        return False


def fetch_recent_data(limit: int = 10) -> list:
    """
    Retrieves the most recent data packages for the frontend dashboard.

    Args:
        limit: The maximum number of records to retrieve.

    Returns:
        A list of dictionaries containing the recent raw payloads.
    """
    if not initialize_db():
        return []

    try:
        with open(DB_FILE_PATH, 'r') as f:
            all_records = json.load(f)

        # The records are already saved in order (oldest first due to append), 
        # so reversing and slicing gives the most recent records.
        recent_records = all_records[::-1][:limit]

        results = []
        for doc in recent_records:
            results.append({
                "id": doc.get('id', 'N/A'),
                # Convert the ISO string back to a datetime object if needed for display/sorting, 
                # but we'll keep it simple here.
                "timestamp": doc.get('fetch_timestamp', 'N/A'),
                "payload": doc.get('raw_payload', {})
            })

        logger.info(f"Successfully fetched {len(results)} recent records from local file.")
        return results

    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from {DB_FILE_PATH}. File may be corrupt.", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Failed to fetch data from local file: {e}", exc_info=True)
        return []