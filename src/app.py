from flask import Flask, jsonify, request
import json
import analysis
import response
import os

app = Flask(__name__)

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Endpoint to retrieve logs.
    """
    with open('incidents.json', 'r') as f:
        incidents = json.load(f)
    return jsonify(incidents)

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to analyze incidents.
    """
    incidents = analysis.load_incidents('incidents.json')
    analyzed_incidents = analysis.analyze_incidents(incidents)
    with open('analyzed_incidents.json', 'w') as f:
        json.dump(analyzed_incidents, f)
    return jsonify(analyzed_incidents)

@app.route('/respond', methods=['POST'])
def respond():
    """
    Endpoint to respond to incidents.
    """
    incidents = response.load_analyzed_incidents('analyzed_incidents.json')
    firewall_url = os.getenv('FIREWALL_API_URL', 'http://127.0.0.1:5000/firewall')  # "Change: Replace hardcoded URL with environment variable"
    results = []
    for incident in incidents:
        result = response.send_to_firewall(firewall_url, incident)
        if incident["result"] == "failure":
            block_result = response.block_ip(firewall_url, incident["ip_address"])
            results.append({"incident": incident, "block_result": block_result, "firewall_result": result})
        else:
            results.append({"incident": incident, "firewall_result": result})
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Make sure the port is different if running on the same machine

