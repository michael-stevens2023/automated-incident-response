import json
from sklearn.ensemble import IsolationForest
import numpy as np

def load_incidents(file_path):
    """
    Load detected incidents from JSON file.

    Args:
        file_path (str): Path to the JSON file containing incidents.

    Returns:
        list: List of incidents.
    """
    with open(file_path, 'r') as f:
        incidents = json.load(f)
    return incidents

def analyze_incidents(incidents):
    """
    Analyze incidents to identify anomalies.

    Args:
        incidents (list): List of detected incidents.

    Returns:
        list: List of analyzed incidents with anomaly scores.
    """
    # Convert incidents to a suitable format for analysis
    data = []
    for incident in incidents:
        try:
            timestamp_hour = int(incident['timestamp'].split('T')[1].split(':')[0])
            ip_last_octet = int(incident['ip_address'].split('.')[-1])
            data.append([timestamp_hour, ip_last_octet])
        except (ValueError, KeyError, IndexError) as e:
            # Handle errors in data conversion
            print(f"Error processing incident {incident}: {e}")
            continue

    data = np.array(data)
    
    if data.shape[0] == 0:
        print("No valid incidents to analyze.")
        return incidents
    
    # Initialize the Isolation Forest model
    model = IsolationForest()
    
    # Fit the model and get anomaly scores
    model.fit(data)
    scores = model.decision_function(data)
    
    for i, incident in enumerate(incidents):
        incident['anomaly_score'] = scores[i] if i < len(scores) else None
    
    return incidents

if __name__ == "__main__":
    # Load detected incidents from JSON file
    incidents = load_incidents('incidents.json')
    
    # Analyze detected incidents for anomalies
    analyzed_incidents = analyze_incidents(incidents)
    
    # Save analyzed incidents to a JSON file
    with open('analyzed_incidents.json', 'w') as f:
        json.dump(analyzed_incidents, f)
    print("Incidents analyzed and saved to analyzed_incidents.json")