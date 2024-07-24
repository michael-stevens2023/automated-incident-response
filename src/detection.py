import json
import requests
import os

def detect_incidents(logs):
    """
    Detect incidents based on log data.

    Args:
        logs (list): List of logs.

    Returns:
        list: List of detected incidents.
    """
    incidents = []
    for log in logs:
        if (log['event_type'] == 'login' and log['result'] == 'failure') or \
           (log['event_type'] == 'file_access' and log['result'] == 'failure') or \
           (log['event_type'] == 'network' and log['result'] == 'failure'):
            incidents.append(log)
    return incidents

if __name__ == "__main__":
    # Fetch logs from the mock API
    api_url = os.getenv("LOGS_API_URL", "http://127.0.0.1:5000/logs")  # Default to local if env variable not set
    response = requests.get(api_url)
    logs = response.json()
    
    # Detect incidents in the logs
    incidents = detect_incidents(logs)
    
    # Save detected incidents to a JSON file
    with open('incidents.json', 'w') as f:
        json.dump(incidents, f)
    print("Incidents detected and saved to incidents.json")
