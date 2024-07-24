import requests
import json
import time
import os

def block_ip(api_url, ip_address):
    """
    Simulate blocking an IP address by sending a request to the firewall API.
    
    Args:
        api_url (str): URL of the firewall API.
        ip_address (str): The IP address to block.
        
    Returns:
        dict: Response from the firewall API.
    """
    data = {
        "action": "block",
        "ip_address": ip_address
    }
    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while blocking IP: {e}")
        return {"status": "error", "message": str(e)}

def process_incidents(api_url, incidents):
    """
    Process each incident, block IP addresses if needed, and save results to a JSON file.
    
    Args:
        api_url (str): URL of the firewall API.
        incidents (list): List of incidents to process.
        
    Returns:
        list: List of results from blocking IP addresses.
    """
    results = []
    for incident in incidents:
        if incident['anomaly_score'] < 0:  # Change threshold as needed
            ip_address = incident['ip_address']
            print(f"Processing IP: {ip_address} with score: {incident['anomaly_score']}")
            result = block_ip(api_url, ip_address)
            results.append({"ip_address": ip_address, "result": result})
    return results

if __name__ == "__main__":
    # URL of the firewall API endpoint
    firewall_api_url = os.getenv('FIREWALL_API_URL', 'http://127.0.0.1:5000/firewall')  # "Change: Replace hardcoded URL with environment variable"

    # Load analyzed incidents from file
    with open('analyzed_incidents.json', 'r') as f:
        analyzed_incidents = json.load(f)

    # Process all incidents
    results = process_incidents(firewall_api_url, analyzed_incidents)

    # Save results to a JSON file
    with open('response_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Response actions completed and results saved to response_results.json")

