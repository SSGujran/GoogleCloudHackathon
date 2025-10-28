# 🏠 Neighborhood Watch Agent

### Built for the Google Agent Hackathon 2025 

[](https://opensource.org/licenses/MIT)
[](https://www.python.org/downloads/)
[](https://www.google.com/search?q=https://github.com/your-repo-link)

## ✨ Project Pitch: Always Know What's Up\!

Tired of sifting through city PDFs, obscure weather feeds, and half-empty neighborhood apps just to know if your street is closed for construction tomorrow? So are we\!

The **Neighborhood Watch Agent** is a streamlined, autonomous digital sentinel built on the Agent Loop model (Perceive $\rightarrow$ Act). It constantly monitors multiple local data sources and immediately publishes a consolidated report, ensuring residents are always the first to know what’s happening—without the AI filtering or overthinking.

This project demonstrates a robust, scheduled data pipeline that prioritizes reliability and transparency.

-----

## 🎯 MVP Goal (Retrieve & Present)

The primary goal of this simplified MVP was to create a reliable, non-LLM-dependent data pipeline:

1.  **Perceive (Sensor Agent):** Hourly collection of raw data from mock external APIs (weather, incidents, events).
2.  **Act (Messenger Agent):** Direct publication of the complete, raw data package to a persistent store.
3.  **Presentation:** Immediate console output of the final data package for verification.

***(Note: The complex LLM-driven "Analyst Agent" was intentionally omitted for simplicity.)***

-----

## 🤖 Architecture Overview: The Two-Step Dance

Our agent system uses a sequential, two-agent pipeline orchestrated by `orchestrator.py`.

### 1\. The Sensor Agent (`agents/sensor_agent.py`) 📡

  * **Role:** The Data Collector.
  * **Action:** Calls various API "tools" (`api_tools.py`) to scrape weather, city incidents, and events.
  * **Output:** A single, structured JSON dictionary (`raw_data_package`) containing all collected inputs.

### 2\. The Messenger Agent (`agents/messenger_agent.py`) 📢

  * **Role:** The Publisher.
  * **Action:** Receives the raw package and calls the data tool (`db_tools.py`) to save it.
  * **Output:** Writes the full package to the local persistent store (`data/alerts.json`).

### 🛠️ Key Tools & Storage

  * **Orchestration:** `orchestrator.py` (Simple Python loop for scheduled execution).
  * **Storage:** Local JSON File (`data/alerts.json`) – **No Firestore/Cloud DB dependency\!**
  * **APIs:** Mocked functions within the `sensor_agent.py` to simulate real-world API calls.

-----

## 🚀 How to Run the Agent

### 1\. Local Setup

First, ensure you have a Python 3.10+ environment active.

1.  **Clone the repository:**

    ```bash
    git clone [your-repo-link]
    cd neighborhood_watch
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Create the required placeholder files:**

    ```bash
    mkdir data
    touch config.py
    touch tools/api_tools.py # Required even though functions are mocked in sensor_agent.py
    ```

    *Note: Ensure your `config.py` contains at least a placeholder for `GCP_PROJECT_ID`.*

### 2\. Execution

To run the entire automated cycle (Perceive $\rightarrow$ Act $\rightarrow$ Show Results):

```bash
python orchestrator.py
```

### Expected Console Output

The script will run the two agents once, save the data, retrieve the latest record, and print it:

```
================================================================================
📢 NEIGHBORHOOD WATCH ALERT DISPLAY 📢
================================================================================

✅ SUCCESS: Retrieved Data Package from ID: 20251028111530123456
   Published Time: 2025-10-28T11:15:30.123456
   Monitored Location: My Local Neighborhood

--- RAW DATA PAYLOAD ---
{
    "fetch_time_utc": "2025-10-28T10:15:30.123456Z",
    "monitoring_location": "My Local Neighborhood",
    "raw_weather": {
        "source": "WeatherAPI",
        "city": "My Local Neighborhood",
        "temperature_c": 18.5,
        "condition": "Partly Cloudy",
        "wind_speed_kph": 25
    },
    "raw_incidents": [
        {
            "type": "Roadwork",
            "location": "Main Street, near City Hall",
            "details": "Lane closure until 18:00.",
            "impact": "High"
        }
    ],
    "raw_ov_updates": []
}

================================================================================
```

-----

## 💻 File Structure & Responsibilities

| File | Type | Responsibility |
| :--- | :--- | :--- |
| `orchestrator.py` | Main | **Triggers the cycle.** Initializes agents and runs the `Sensor -> Messenger` flow once. |
| `agents/sensor_agent.py` | Agent | **PERCEIVE.** Collects and packages raw data from mocked external tools. |
| `agents/messenger_agent.py` | Agent | **ACT/PRESENT.** Receives raw data and passes it to `db_tools` for saving. |
| `tools/db_tools.py` | Tool | **STORAGE.** Manages reading/writing the JSON records to the local `data/alerts.json` file. |
| `tools/api_tools.py` | Tool | *(Placeholder)* Would contain actual external API call logic. |
| `requirements.txt` | Config | Lists minimal dependencies (`langchain-core`, `requests`). |
| `config.py` | Config | Environment variables (e.g., `GCP_PROJECT_ID`). |

-----

## 🔮 Future Enhancements (If we had more time\!)

1.  **Reintroduce the Analyst:** Integrate the **Gemini/Vertex AI LLM** to perform **summarization**, **relevance filtering**, and **alert generation**.
2.  **Live Frontend:** Implement the Streamlit dashboard (`app.py`) using the saved data for real-time visualization.
3.  **Cloud Deployment:** Deploy the `orchestrator.py` to **Google Cloud Run** and use **Cloud Scheduler** for robust, hourly execution.
4.  **Real Data Integration:** Replace mock functions with calls to actual open-source city or weather APIs.
